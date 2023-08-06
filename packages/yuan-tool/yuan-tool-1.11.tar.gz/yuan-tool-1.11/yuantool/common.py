import yaml
import platform
import string
import os
import sys
import hashlib
import binascii
import re
import random
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode, urljoin
from .iptool.iptool import is_ip


def check_keys(require_keys, request_keys):
    flag = True
    lost_key = None
    for key in require_keys:
        if not (key in request_keys.keys() and request_keys[key]):
            flag = False
            lost_key = key
    return flag, lost_key


def format_url(url):
    res = urlparse(url)
    scheme = res.scheme + '://' if res.scheme else 'http://'
    if res.scheme and not res.hostname:
        scheme = 'http://' if str(res.port) != '443' else 'https://'
        host = str(res.scheme)
        path = str(res.path)
        if res.scheme == 'http':
            port = str(res.port) if res.port else "80"
        else:
            port = str(res.port) if res.port else "443"
    elif res.scheme:
        if res.scheme == 'http':
            port = str(res.port) if res.port else "80"
        else:
            port = str(res.port) if res.port else "443"
        if '/' in str(res.hostname):
            host = str(res.hostname).split('/')[0]
            path = '/' + ''.join(str(res.hostname).split('/')[0:]) + str(res.path)
        else:
            host = str(res.hostname)
            path = str(res.path)
    else:
        port = str(res.port) if res.port else '80'
        if '/' in str(res.path):
            t = str(res.path).split('/')
            host = str(res.path).split('/')[0]
            path = '/' + ''.join(str(res.path).split('/')[1:])
        else:
            host = res.path
            path = ''
    if is_ip(host):
        if path:
            return scheme + host + path
        else:
            return scheme + host + ":" + port
    else:
        if host.startswith('www.'):
            r = scheme + host
        elif host.startswith('host.docker.internal'):
            if port != '80' and port != '443':
                r = scheme + host + ':' + port
            else:
                r = scheme + host
        else:
            r = scheme + 'www.' + host
        return r + path


def switch_api_from_url(url, api_path):
    """
    更改api，保留其他参数
    :param url: 原始url
    :param api_path: 新的api地址（不需要一开始的/）
    :return:
    """
    res = urlparse(url)
    # scheme, netloc, path, params, query, fragment
    res_com = (res.scheme, res.netloc, api_path, res.params, res.query, res.fragment)
    res = urlunparse(res_com)
    return res


def parse_params_for_url(url, dic):
    """在原有的url基础上增加新的query参数字典"""
    res = urlparse(url)
    query = urlencode(dic)
    res_com = (res.scheme, res.netloc, res.path, res.params, '{}&{}'.format(res.query, query), res.fragment)
    res = urlunparse(res_com)
    return res


def set_vul_task_id(ip, report_url):
    try:
        task = parse_qs(urlparse(report_url).query)['task_id'][0]
        process = parse_qs(urlparse(report_url).query)['process'][0]
        task_id = task + '_' + process + '_' + str(ip)
        return {'vul_task_id': task_id}
    except:
        return {}


def read_yaml(config_path, config_name=''):
    """
    config_path:配置文件路径
    config_name:需要读取的配置内容,空则为全读
    """
    if config_path:
        with open(config_path, 'r', encoding="utf-8") as f:
            conf = yaml.safe_load(f.read())  # yaml.load(f.read())
        if not config_name:
            return conf
        elif config_name in conf.keys():
            return conf[config_name.upper()]
        else:
            raise KeyError('未找到对应的配置信息')
    else:
        raise ValueError('请输入正确的配置名称或配置文件路径')


def read_file_index(file_path):
    with open(file_path, 'r', encoding="utf-8") as f:
        num = f.readline()
    return int(num)


def save_file_index(file_path, cnt):
    with open(file_path, 'w+', encoding="utf-8") as f:
        f.write(str(cnt))


def hex_to_bytes(s: str):
    return binascii.a2b_hex(s)


def md5(s: str, encoding='utf-8'):
    return hashlib.md5(s.encode(encoding=encoding)).hexdigest()


def getattr_value(arr, key):
    return getattr(arr, key) if key in arr else ''


def read_file(file, encoding='utf-8'):
    """
    :param file: 文件名
    :param encoding: 编码，默认utf-8
    :return:
    """
    with open(file, 'r', encoding=encoding) as f:
        return f.read()


def where_is(program):
    """
    Protected method enabling the object to find the full path of a binary
    from its PATH environment variable.
    :param program: name of a binary for which the full path needs to
    be discovered.
    :return: the full path to the binary.
    :todo: add a default path list in case PATH is empty.
    """
    __is_windows = (platform.system() == 'Windows')
    split_char = ';' if __is_windows else ':'
    program = program + '.exe' if __is_windows else program
    paths = os.environ.get('PATH', '').split(split_char)
    for path in paths:
        if (os.path.exists(os.path.join(path, program)) and not
        os.path.isdir(os.path.join(path, program))):
            if not platform.system() == 'Windows':
                return os.path.join(path, program)
            else:
                return '\"' + os.path.join(path, program) + '\"'
    return None


def get_real_link(bath_path: str):
    """
    传入文件的绝对路径，返回文件的源文件的绝对路径
    :param bath_path:
    :return:
    """
    if os.path.islink(bath_path):
        real_link = os.readlink(bath_path)
        bath_path = os.path.abspath(os.path.dirname(bath_path))
        path = os.path.join(bath_path, real_link)
        return get_real_link(path)
    else:
        return bath_path


def is_vars(keys, obj):
    '''
    判断对象中是否存在多个键值
    keys和obj必须都为集合
    return:
        success: Boolean 是否全部包含
        unhave: Dict    不存在keys的集合
    '''
    success = False
    try:
        result = keys.intersection(obj)
        unhave = keys - result
        dis = len(keys) - len(result)
        # 判断是否keys全部存在
        if dis == 0:
            success = True

        return success, unhave
    except AttributeError as e:
        print(e)


def format_name(name):
    name = re.sub('[\s\-]+', '_', name)

    return name.lower()


def qs_strr(s):
    data = {}
    if len(s) > 0:
        for key in s:
            data[key] = s[key][0]

    return data


# 初始化数据
def init_data(keys, value=None):
    v = {}
    for key in keys:
        v[key] = value

    return v


# 将json转化为字符串，\n分割
def json_to_warp_str(json):
    s = ''
    for key in json:
        s += f'{key}: {json[key]}\n'
    return s


# 数据过滤
def data_filter(data):
    data = re.sub(r'\s', '', data)

    return data


def list_to_dict(l):
    ''' list 转 dict类型 '''
    d = {i for i in l}
    return d


def get_filename(file):
    ''' 获取文件名 '''
    return file[:file.find('.')]


def dataToStdout(data, bold=False):
    """
    Writes text to the stdout (console) stream
    """

    sys.stdout.write(data)

    try:
        sys.stdout.flush()
    except IOError:
        pass

    return


def get_parent_paths(path, domain=True):
    '''
    通过一个链接分离出各种目录
    :param path:
    :param domain:
    :return:
    '''
    netloc = ''
    if domain:
        p = urlparse(path)
        path = p.path
        netloc = "{}://{}".format(p.scheme, p.netloc)
    paths = []
    if not path or path[0] != '/':
        return paths
    # paths.append(path)
    if path[-1] == '/':
        paths.append(netloc + path)
    tph = path
    if path[-1] == '/':
        tph = path[:-1]
    while tph:
        tph = tph[:tph.rfind('/') + 1]
        paths.append(netloc + tph)
        tph = tph[:-1]
    return paths


def get_links(content, domain, limit=True):
    '''
    从网页源码中匹配链接
    :param content: html源码
    :param domain: 当前网址domain
    :param limit: 是否限定于此域名
    :return:
    '''
    p = urlparse(domain)
    netloc = "{}://{}{}".format(p.scheme, p.netloc, p.path)
    match = re.findall(r'''(href|src)=["'](.*?)["']''', content, re.S | re.I)
    urls = []
    for i in match:
        _domain = urljoin(netloc, i[1])
        if limit:
            if p.netloc.split(":")[0] not in _domain:
                continue
        urls.append(_domain)
    return urls


def random_str(length=10, chars=string.ascii_lowercase):
    return ''.join(random.sample(chars, length))
