import re
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode, urljoin
from .iptool.iptool import is_ip


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
