import os
import subprocess
import sys
import json
import shlex
import shutil
import logging

from ._analyze import Wappalyzer
from .technologies import Technologies
from .common import perform, get_orignal_url
from .cert_ana import CertInfo
from yuantool.path import abs_find_program as where_is

logger = logging.getLogger(__name__)
logger.name = 'wappalyzer'


class WappalyzerWrapper(object):
    TIMEOUT = 500

    def __init__(self, wappalyzerpath=None, wappalyzerargs=None, enforce_python=False):
        """
        verbose：是否输出详细信息
        wappalyzerpath: 是否有指定wappalyzer的路径，有就直接用
        wappalyzerargs: 指定wappalyzer的函数，备用
        enforce_python: 如果是True，则强制使用python的requests配合指纹json数据分析

        注意：enforce_python和wappalyzerpath同时指定也是选择使用python
        """
        # 如果没有path，寻找系统里是否有
        if not wappalyzerpath:
            if shutil.which("wappalyzer"):
                self.wappalyzerpath = ['wappalyzer']
            # 寻找docker里是否有
            elif shutil.which("docker"):
                # Test if docker image is installed
                o = subprocess.run(args=['docker', 'image', 'ls'], stdout=subprocess.PIPE)
                if 'wappalyzer/cli' not in o.stdout.decode():
                    self.wappalyzerpath = None
                else:
                    self.wappalyzerpath = ['docker', 'run', '--rm', 'wappalyzer/cli']
            # 尽力惹
            else:
                self.wappalyzerpath = None
        # 如果有指定wappalyzerpath，就直接使用
        else:
            self.wappalyzerpath = shlex.split(wappalyzerpath)
        # 如果没有path，就是用python的requests加json数据
        if not self.wappalyzerpath:
            self.wappalyzerargs = None
            self.python = True

        # 强制使用requests，目前用于ipv6的情况
        elif enforce_python:
            self.python = True

        else:
            self.wappalyzerargs = shlex.split(wappalyzerargs) if wappalyzerargs else []
            self.python = False

        if self.python:
            logger.debug("Using python-Wappalyzer")
            self.wappalyzer = Wappalyzer.latest(Technologies.project_file)
        else:
            logger.debug("Using Wappalyzer CLI: {}".format(' '.join(self.wappalyzerpath)))

        self.results = []

    def analyze(self, webpage):

        host = webpage.url

        if self.python:

            logger.debug("Analyzing {} with python-Wappalyzer".format(host))
            try:
                apps = self.wappalyzer.neo_analyze_with_versions_and_categories(webpage)

                logger.debug("{} technologies: {}".format(host, apps))

                # Make the format like the real Wappalyzer with the minimal infos
                # Works with python-Wappalyzer
                result = dict()
                result['urls'] = {host: {'status': str(webpage.status_code)}}
                result['technologies'] = list()

                for tech_name, infos in apps.items():
                    # 'technologies': [
                    #     {'slug': 'nginx', 'name': 'Nginx', 'confidence': 100, 'version': None, 'icon': 'Nginx.svg',
                    #      'website': 'http://nginx.org/en', 'cpe': 'cpe:/a:nginx:nginx',
                    #      'categories': [{'id': 22, 'slug': 'web-servers', 'name': 'Web servers'},
                    #                     {'id': 64, 'slug': 'reverse-proxies', 'name': 'Reverse proxies'}]}]
                    infos['version'] = infos.pop('versions') if 'versions' in infos else ''
                    infos['confidence'] = '100'
                    tmp = []
                    for cat in infos['categories']:
                        tmp.append({"name": cat})
                    infos['categories'] = tmp
                    app_dict = dict()
                    app_dict['name'] = tech_name
                    app_dict.update(infos)
                    result['technologies'].append(app_dict)

            except Exception as e:
                raise RuntimeError(str(e))

        elif self.wappalyzerpath:

            cmd = self.wappalyzerpath + [host] + self.wappalyzerargs
            logger.debug("Analyzing: " + str(cmd))

            try:
                p = subprocess.run(cmd, bufsize=100000, timeout=self.TIMEOUT, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=sys.platform != "win32")
                logger.debug("{} technologies: {}".format(host, p.stdout))

                if p.returncode == 0:
                    result = json.loads(p.stdout)
                else:
                    raise RuntimeError("Wappalyzer failed:\n{}{}".format(p.stdout.decode(), p.stderr.decode()))

            except subprocess.TimeoutExpired:
                raise RuntimeError('Analyzing {} too long, process killed.'.format(host))
            except OSError:
                raise RuntimeError('Too many analyzing stuff, process killed.'.format(host))
            except:
                raise RuntimeError('Unknown error occurred in  analyzing stuff, process killed.'.format(host))
        else:
            raise RuntimeError('No Wappalyzer engine')

        self.results.append(result)
        return result

    def gather_web_info(self, webpage):
        # 收集页面信息（针对于nmap没有获取到title的情况则要进行mark，二度访问页面）
        # mark于nmap_scan.py里设置

        if hasattr(webpage, 'mark') and webpage.mark:
            # 为了获取页面内容进行request，如果是调用request的那种（python==True的情况），直接就进行parse了
            webpage.do_request()
        if self.python:
            # parse:整理页面数据，分类出meta，html，scripts等要素供后续分析
            webpage.do_parse_html()

    def gather_cert_info(self, webpage):
        if "https://" not in webpage.url:
            webpage.cert = {}
        else:
            try:
                webpage.cert = CertInfo(webpage.url).get_info()
            except Exception as e:
                logger.error(e, exc_info=True)
                webpage.cert = {}


class EnormWappalyzer(object):
    wappalyzerpath = where_is('wappalyzer')
    asynch_workers = 5

    def __init__(self, webpages, asynch_workers=asynch_workers, **kwargs):

        logger.info('开始分析Web资产指纹信息，可能会耗费一些时间')

        if isinstance(webpages, list):
            self.webpages = webpages
        else:
            self.webpages = [webpages]
        self.asynch_workers = asynch_workers
        self.analyzer = WappalyzerWrapper(wappalyzerpath=self.wappalyzerpath,
                                          **kwargs)
        self._old_analyzed_fp = []
        self._analyzed_fp = []

    def run(self):
        # 根据需求，针对性的对每个webpage进行请求等操作
        try:
            perform(self.analyzer.gather_web_info,
                    self.webpages,
                    asynch=True,
                    workers=self.asynch_workers,
                    progress=True)
        except Exception as e:
            logger.warning(e, exc_info=True)
        # 分析每个webpage
        try:
            self.raw_results = perform(
                self.analyzer.analyze,
                self.webpages,
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
            # self.set_analyzed_fp(self.raw_results)
            # self.set_old_analyzed_fp(self.raw_results)
            return True
        except KeyboardInterrupt:
            logger.info("用户停止指纹探测")
            return False
        except Exception as e:
            logger.warning(e, exc_info=True)
            return False

    @property
    def es_web_info(self):
        """
        用于存储到es的完整数据
        :return:
        """
        # 增加证书部分，暂时先放在这
        perform(self.analyzer.gather_cert_info,
                self.webpages,
                asynch=True,
                workers=self.asynch_workers,
                progress=True)

        for item in self.raw_results:
            url = get_orignal_url(item)
            # 将这个fp给对应的webpages
            for webpage in self.webpages:
                if webpage.url == url:
                    for d in item['technologies']:
                        try:
                            del d['icon']
                            del d['website']
                        except:
                            pass
                    webpage.analyzed_fp = item['technologies']

        http_info = []
        for webpage in self.webpages:
            # 再次进行网页请求，完善html信息，响应头等信息
            # webpage.do_request()
            target = {'title': webpage.title, 'status_code': webpage.status_code, 'target': webpage.url}
            if hasattr(webpage, 'html'):
                try:
                    target['html'] = webpage.html.decode('utf-8')
                except:
                    target['html'] = webpage.html
            if hasattr(webpage, 'headers'):
                target['headers'] = webpage.headers
            if hasattr(webpage, 'analyzed_fp'):
                target['fingerprints'] = webpage.analyzed_fp
            if hasattr(webpage, 'cert') and webpage.cert:
                target['cert'] = webpage.cert
                # 清理不需要的数据
                del target['cert']['Parameter']
            http_info.append(target)
        return http_info

    @property
    def old_web_info(self):
        """
        after
        fingerprint = {'Web server':['Nginx','Tomcat'],'JavaScript libraries':['lodash']}
        """
        # 处理fp结果格式
        for item in self.raw_results:
            url = get_orignal_url(item)
            fingerprint = {}
            for technology in item['technologies']:
                for cat in technology['categories']:
                    if cat['name'] in fingerprint:
                        fingerprint[cat['name']].append(technology['name'])
                    else:
                        fingerprint[cat['name']] = [technology['name']]

            # 将这个fp给对应的webpages
            for webpage in self.webpages:
                # 3.0做的小修改
                if url.startswith(webpage.url):
                    webpage.old_analyzed_fp = fingerprint
                if not webpage.status_code:
                    try:
                        webpage.status_code = item['urls'][list(item['urls'])[0]]['status']
                    except:
                        pass

        http_info = []
        for webpage in self.webpages:

            target = {'title': webpage.title, 'status_code': webpage.status_code, 'target': webpage.url}
            try:
                if webpage.old_analyzed_fp:
                    if 'Web servers' in webpage.old_analyzed_fp:
                        webpage.old_analyzed_fp['webserver'] = webpage.old_analyzed_fp.pop('Web servers')
                    if 'Web frameworks' in webpage.old_analyzed_fp:
                        webpage.old_analyzed_fp['webframework'] = webpage.old_analyzed_fp.pop('Web frameworks')
                    target['fingerprint'] = webpage.old_analyzed_fp
            except Exception as e:
                logger.error("web指纹出错：{}".format(e), exc_info=True)
            http_info.append(target)
        return http_info
