import re
import socket
import requests
import json
import logging
from IPy import IP

from .geolite.geolite import GeoLite
from .cz.cz import CzIp

logger = logging.getLogger(__name__)
logger.name = 'ip_module'


def _get_html(url):
    # change_user_agent()
    html = requests.get(url)
    if html.status_code == 200:
        res = html.text
    else:
        res = False
    return res


def _post_data(url, data):
    # change_user_agent()
    try:
        res = requests.post(url, data=str(data).encode('utf-8'))
        if res.status_code != 200:
            res = False
    except Exception as e:
        if 'Failed to establish a new connection:' in str(e):
            logger.warning(e)
            logger.warning(e)
        else:
            logger.warning(e, exc_info=True)
        res = False
    return res


def get_addr_from_ip_by_whois(target):
    try:
        api = f'http://whois.pconline.com.cn/ipJson.jsp?ip={target}&json=true'
        info = _get_html(api)
        info = json.loads(info)
        info = json.loads(info)
        res = info
    except Exception as e:
        logger.warning(e, exc_info=True)
        res = False
    return res


def get_jw_from_addr_by_mapqq(city):
    try:
        api = 'https://apis.map.qq.com/jsapi?qt=poi&wd=' + city
        info = _get_html(api)
        info = json.loads(info)
        pointx = info['detail']['city']['pointx']
        pointy = info['detail']['city']['pointy']
    except Exception as e:
        print(e)
        print(city)
        print(api)
        print(info)
        pointx = 0
        pointy = 0
    return pointx, pointy


def get_fingerprint_from_ip_by_whatweb(target):
    api = 'http://whatweb.bugscaner.com/what.go'
    _data = {'url': target, 'location_capcha': 'no'}
    try:
        info = _post_data(api, _data)
        print('获取信息', info)
        if info:
            res = info
        else:
            res = False
    except Exception as e:
        logger.warning(e)
        res = False
    return json.loads(res.text)


def is_domain(domain):
    if re.match('(.+?\.)+[a-zA-Z0-9]+', domain):
        res = True
    else:
        res = False
    return res


def is_ip(target):
    return is_ipv6(target) or is_ipv4(target)


def is_ipv6(target):
    return re.search(
        r'^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$',
        target)


def is_ipv4(target):
    try:
        return re.search(r'^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}$', target)
    except:
        return None


def is_ip_cidr(target):
    return re.search(
        r'^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}\/(([12]{0,1}[0-9])|(3[0-2]))$',
        target)


def split_cidr(target):
    return [str(i) for i in IP(target)]


def get_ip_from_target(target):
    try:
        domain = get_domain(target)
        myaddr = socket.getaddrinfo(domain, 'http')
        return myaddr[0][4][0]
    except socket.gaierror:
        logger.warning("{}未能找到ip".format(target))
        return None


def get_domain(site):
    if site.startswith('http://'):
        site = site[7:]
    elif site.startswith("https://"):
        site = site[8:]
    if site.endswith('/'):
        site = site[:-1]
    return site


def get_info_by_ip(ip):
    return GeoLite.get_info_by_ip(ip)


def get_info_by_target(target):
    ip = get_ip_from_target(target)
    return GeoLite.get_info_by_ip(ip)


def get_info_by_ip_from_cz(ip):
    cz = CzIp()
    # print(cz.get_version())
    # print(cz.get_ip_range(ip))
    res = cz.get_addr_by_ip(ip)
    return res
