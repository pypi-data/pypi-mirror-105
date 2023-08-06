# !/usr/bin/env python3

# Run Wappalyzer asynchronously on a list of URLs and generate a excel file with all Wappalyzer informations

import subprocess
import sys
import json
import shlex
from urllib.parse import urlparse
import functools
import concurrent.futures
import re
from collections import namedtuple
import shutil
import requests


##### Static methods

def ensure_keys(dictionnary, keys, default_val=""):
    row = namedtuple('row', list(set(list(dictionnary.keys()) + list(keys))))
    row.__new__.__defaults__ = (default_val,) * len(row._fields)  # set default values to empty string if not specified
    return row(**dictionnary)._asdict()


def get_valid_filename(s):
    '''Return the given string converted to a string that can be used for a clean filename.  Stolen from Django I think'''
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


def clean(s):
    # Remove invalid characters
    s = re.sub('[^0-9a-zA-Z_]', '', s)
    # Remove leading characters until we find a letter or underscore
    s = re.sub('^[^a-zA-Z_]+', '', s)
    if s.isnumeric(): s = '_' + s
    return s


def perform(func, data, func_args=None, asynch=False, workers=None, progress=False, desc='Loading...'):
    """
    Wrapper arround executable and the data list object.
    Will execute the callable on each object of the list.
    Parameters:

    - `func`: callable stateless function. func is going to be called like `func(item, **func_args)` on all items in data.
    - `data`: if stays None, will perform the action on all rows, else it will perfom the action on the data list.
    - `func_args`: dict that will be passed by default to func in all calls.
    - `asynch`: execute the task asynchronously
    - `workers`: mandatory if asynch is true.
    - `progress`: to show progress bar with ETA (if tqdm installed).
    - `desc`: Message to print if progress=True
    Returns a list of returned results
    """
    if not callable(func):
        raise ValueError('func must be callable')
    # Setting the arguments on the function
    func = functools.partial(func, **(func_args if func_args is not None else {}))
    # The data returned by function
    returned = list()
    elements = data
    try:
        import tqdm
    except ImportError:
        progress = False
    tqdm_args = dict()
    # The message will appear on loading bar if progress is True
    if progress is True:
        tqdm_args = dict(desc=desc, total=len(elements))
    # Runs the callable on list on executor or by iterating
    if asynch:
        if isinstance(workers, int):
            if progress:
                returned = list(tqdm.tqdm(concurrent.futures.ThreadPoolExecutor(
                    max_workers=workers).map(
                    func, elements), **tqdm_args))
            else:
                returned = list(concurrent.futures.ThreadPoolExecutor(
                    max_workers=workers).map(
                    func, elements))
        else:
            raise AttributeError('When asynch == True : You must specify a integer value for workers')
    else:
        if progress:
            elements = tqdm.tqdm(elements, **tqdm_args)
        for index_or_item in elements:
            returned.append(func(index_or_item))
    return returned


##### Core

class WappalyzerWrapper(object):
    TIMEOUT = 500

    def __init__(self, verbose=False, wappalyzerpath=None, wappalyzerargs=None, python=False):
        if not wappalyzerpath:

            if shutil.which("wappalyzer"):
                self.wappalyzerpath = ['wappalyzer']

            elif shutil.which("docker"):
                # Test if docker image is installed
                o = subprocess.run(args=['docker', 'image', 'ls'], stdout=subprocess.PIPE)
                if 'wappalyzer/cli' not in o.stdout.decode():
                    self.wappalyzerpath = None
                else:
                    self.wappalyzerpath = ['docker', 'run', '--rm', 'wappalyzer/cli']
            else:
                self.wappalyzerpath = None
        else:
            self.wappalyzerpath = shlex.split(wappalyzerpath)

        if not self.wappalyzerpath:
            self.wappalyzerargs = None
            self.python = True

        elif python:
            self.python = True

        else:
            self.wappalyzerargs = shlex.split(wappalyzerargs) if wappalyzerargs else []
            self.python = False

        self.verbose = verbose

        if self.python:
            print("Using python-Wappalyzer")
            try:
                from Wappalyzer import Wappalyzer, WebPage
                self.webpage = WebPage.new_from_url
                lastest_technologies_file = requests.get(
                    'https://raw.githubusercontent.com/AliasIO/wappalyzer/master/src/technologies.json')
                with open('/tmp/lastest_technologies_file.json', 'w') as t_file:
                    t_file.write(lastest_technologies_file.text)
                self.wappalyzer = Wappalyzer.latest(technologies_file='/tmp/lastest_technologies_file.json')

            except ImportError:
                print("Please install python-Wappalyzer")
                exit(1)
        else:
            print("Using Wappalyzer CLI: {}".format(' '.join(self.wappalyzerpath)))

        self.results = []

    def analyze(self, host):

        # Strip URL string
        host = host.strip()
        # Format URL with scheme indication if not already present
        p_url = list(urlparse(host))
        if p_url[0] == "":
            host = 'http://' + host
        result = None

        if self.python:

            if self.verbose:
                print("Analyzing {} with python-Wappalyzer".format(host))
            try:
                apps = self.wappalyzer.analyze_with_versions_and_categories(self.webpage(host))

                if self.verbose:
                    print("{} technologies: {}".format(host, apps))

                # Make the format like the real Wappalyzer with the minimal infos
                # Works with python-Wappalyzer 0.2.3
                result = dict()
                result['urls'] = {host: {'status': 'OK'}}
                result['applications'] = list()

                for tech_name, infos in apps.items():
                    app_dict = dict()
                    app_dict['name'] = tech_name
                    app_dict.update(infos)
                    result['applications'].append(app_dict)

            except Exception as e:
                return RuntimeError(str(e))

        elif self.wappalyzerpath:

            cmd = self.wappalyzerpath + [host] + self.wappalyzerargs
            if self.verbose: print("Analyzing: " + str(cmd))

            try:
                if sys.platform.startswith('freebsd') \
                        or sys.platform.startswith('linux') \
                        or sys.platform.startswith('darwin'):
                    p = subprocess.run(cmd, bufsize=100000, timeout=self.TIMEOUT, stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                else:
                    p = subprocess.run(cmd, bufsize=100000, timeout=self.TIMEOUT, stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                if self.verbose:
                    print("{} technologies: {}".format(host, p.stdout))

                if p.returncode == 0:
                    result = json.loads(p.stdout)
                else:
                    return RuntimeError("Wappalyzer failed:\n{}{}".format(p.stdout.decode(), p.stderr.decode()))

            except subprocess.TimeoutExpired:
                return RuntimeError('Analyzing {} too long, process killed.'.format(host))
        else:
            return RuntimeError('No Wappalyzer engine')

        self.results.append(result)
        return result


class MassWappalyzer(object):

    def __init__(self,
                 urls,
                 asynch_workers=5,
                 verbose=False,
                 **kwargs):

        print('Mass Wappalyzer')

        self.urls = urls
        self.asynch_workers = asynch_workers
        self.verbose = verbose

        self.analyzer = WappalyzerWrapper(
            verbose=verbose, wappalyzerpath='/usr/local/bin/wappalyzer',
            **kwargs)
        self._old_analyzed_fp = []
        self._analyzed_fp = []

    def run(self):

        try:
            raw_results = perform(
                self.analyzer.analyze,
                self.urls,
                asynch=True,
                workers=self.asynch_workers,
                progress=True)

            # The dict looks like this:
            """
            original:
            {'urls': {'http://103.44.144.41/': {'status': 302}, 'http://103.44.144.41/login': {'status': 200}},
             'technologies': [
                 {'slug': 'nginx', 'name': 'Nginx', 'confidence': 100, 'version': None, 'icon': 'Nginx.svg',
                  'website': 'http://nginx.org/en', 'cpe': 'cpe:/a:nginx:nginx',
                  'categories': [{'id': 22, 'slug': 'web-servers', 'name': 'Web servers'},
                                 {'id': 64, 'slug': 'reverse-proxies', 'name': 'Reverse proxies'}]},
                 {'slug': 'webpack', 'name': 'webpack', 'confidence': 100, 'version': None, 'icon': 'webpack.svg',
                  'website': 'https://webpack.js.org/', 'cpe': None,
                  'categories': [{'id': 19, 'slug': 'miscellaneous', 'name': 'Miscellaneous'}]},
                 {'slug': 'underscore-js', 'name': 'Underscore.js', 'confidence': 0, 'version': '4.17.11',
                  'icon': 'Underscore.js.png', 'website': 'http://underscorejs.org', 'cpe': None,
                  'categories': [{'id': 59, 'slug': 'javascript-libraries', 'name': 'JavaScript libraries'}]},
                 {'slug': 'lodash', 'name': 'Lodash', 'confidence': 100, 'version': '4.17.11', 'icon': 'Lo-dash.png',
                  'website': 'http://www.lodash.com', 'cpe': 'cpe:/a:lodash:lodash',
                  'categories': [{'id': 59, 'slug': 'javascript-libraries', 'name': 'JavaScript libraries'}]},
                 {'slug': 'babel', 'name': 'Babel', 'confidence': 100, 'version': None, 'icon': 'Babel.svg',
                  'website': 'https://babeljs.io', 'cpe': None,
                  'categories': [{'id': 19, 'slug': 'miscellaneous', 'name': 'Miscellaneous'}]}]}
            """

            self.set_analyzed_fp(raw_results)
            self.set_old_analyzed_fp(raw_results)
            return True
        except KeyboardInterrupt:
            print("用户停止指纹探测")
            return False
        except Exception as e:
            print(e)
            return False

    def get_analyzed_fp(self):
        if not self.analyzer.results:
            print('尚未进行扫描')
            return False
        else:
            if len(self.urls) == 1:
                return self._analyzed_fp[0]
            else:
                return self._analyzed_fp

    def set_analyzed_fp(self, result):
        """
        after
        fingerprints = {'Nginx': {"version": "None", "confidence": 100}, "webpack": {'version': "None", "confidence": 100}}
        """
        result_ = []
        for item in result:
            fingerprints = {}
            for technology in item['technologies']:
                fingerprints[technology['name']] = {'version': technology['version'],
                                                    'confidence': technology['confidence']}
            result_.append(fingerprints)

        self._analyzed_fp = result_

    def get_old_analyzed_fp(self):
        if not self.analyzer.results:
            print('尚未进行扫描')
            return {}
        else:
            if len(self.urls) == 1:
                return self._old_analyzed_fp[0]
            else:
                return self._old_analyzed_fp

    def set_old_analyzed_fp(self, result):
        """
        after
        fingerprint = {'Web server':['Nginx','Tomcat'],'JavaScript libraries':['lodash']}
        """
        result_ = []
        for item in result:
            fingerprint = {}
            for technology in item['technologies']:
                for cat in technology['categories']:

                    if cat['name'] in fingerprint:
                        fingerprint[cat['name']].append(technology['name'])

                    else:
                        fingerprint[cat['name']] = [technology['name']]

            result_.append(fingerprint)
        self._old_analyzed_fp = result_


def main():
    # args = vars(parse_arguments())

    urls = ["http://0.0.0.0:1220/upload"]

    mass_w = MassWappalyzer(urls, python=False, verbose=True)

    if mass_w.run():
        mass_w.get_analyzed_fp()
        mass_w.get_old_analyzed_fp()


if __name__ == "__main__":
    main()
