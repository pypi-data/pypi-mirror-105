import ssl
import requests
import chardet
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from .cert_ana import CertInfo

disable_warnings(InsecureRequestWarning)


class TLSv1_1_HttpAdapter(HTTPAdapter):
    """"Transport adapter" that allows us to use TLSv1.1"""

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1_1)


tls_httpadapter = TLSv1_1_HttpAdapter()

"""
webpage现在有三种情况
一种直接进来所有的数据，并且进行分析
一种进来url，进行request，进行分析
一种进来url，进行request，不进行分析
"""


# 指纹分析用model
class WebPage(object):
    """
    Simple representation of a web page, decoupled
    from any particular HTTP library's API.
    """

    request_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    }

    def __init__(self, url: str, **kwargs):
        """
        Initialize a new WebPage object.

        Parameters
        ----------

        :param url: The web page URL.
        :param html: (optional) The web page content (HTML)
        headers : dict
            The HTTP response headers
        verify:bool
            The HTTPS do verify?
        do_request:bool
            If True,do real request,or read kwargs
        """
        self.url = url
        self.domain = urlparse(self.url).hostname
        self.product = kwargs.get('product') if 'product' in kwargs else ''
        self.headers = kwargs.get('headers') if 'headers' in kwargs else {}
        self.html = kwargs.get('body') if 'body' in kwargs else ''
        if self.html:
            self.soup = BeautifulSoup(self.html, 'lxml')
            self.title = self.soup.title.string if self.soup.title else ''
        else:
            self.title = ''
        self.status_code = kwargs.get('status_code') if 'status_code' in kwargs else None
        # 解决 DH key too small报错
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
        self.s = requests.Session()
        self.s.verify = False

        # 增加cert指纹识别（暂时没用
        self.cert_analyze = True if 'cert_scan' in kwargs and kwargs['cert_scan'] else False

    def do_request_with_parse(self):
        # 做一遍request，并最后会根据请求的结果更新网页数据
        self.do_request()
        self.do_parse_html()

    def do_request(self):
        # 做一遍request，并最后会根据请求的结果更新网页数据
        if self.url.startswith("http://"):
            self.parse_http()
        elif self.url.startswith("https://"):
            self.parse_https()
        else:
            self.url = 'http://' + self.url
            self.parse_http()

    def parse_http(self, allow_redirects=True):
        self.https_to_http()
        try:
            response = self.s.get(self.url, timeout=5, headers=self.request_headers,
                                  allow_redirects=allow_redirects)
            self._parse_response(response)
        except requests.exceptions.SSLError:
            if not allow_redirects:
                self._parse_response()
            # 重定向去了ssl网页
            self.parse_https()
        except Exception as e:
            if 'Read timed out' in str(e):
                print("网站{}链接超时,无法访问".format(self.url))
            else:
                # case1 :http://103.44.144.193:646
                print("{} 访问失败，错误代码:{}".format(self.url, e))
            self._parse_response()

    def parse_https(self):
        self.http_to_https()
        try:
            self.cert_info = CertInfo(self.url).get_info()
        except Exception as e:
            pass
        try:
            response = self.s.get(self.url, timeout=5, headers=self.request_headers)
            self._parse_response(response)
        except requests.exceptions.InvalidURL:
            print("url{}错误".format(self.url))
            self._parse_response()
        except ssl.SSLError as e:
            print("发生错误{},\n 尝试使用http再次进行访问{}".format(e, self.url))
            self.parse_http(allow_redirects=False)
        except requests.exceptions.SSLError:
            # case :https://103.44.144.85:18443 ,TLSv1.1可以访问
            # 给这个SSL错误的url一个机会，更改一下传输适配器的版本试试
            try:
                self.s.mount(self.url, tls_httpadapter)
                response = self.s.get(self.url, timeout=5)
                self._parse_response(response)
            except Exception as e:
                print("{}更改为TLSv1.1访问依然失败，报错为{},尝试使用http访问".format(self.url, e))
                self.parse_http(allow_redirects=False)
        except Exception as e:
            print("{} 访问失败，错误代码:{}".format(self.url, e))
            self.parse_http(allow_redirects=False)

    def _parse_response(self, response=None):
        """
        对response内容进行处理
        :param response:
        :return:
        """
        if response:
            # if use response.text, could have some error
            self.html = response.content
            self.soup = BeautifulSoup(self.html, 'lxml')
            self.title = self.soup.title.string if self.soup.title else ''
            self.status_code = response.status_code
            self.headers = dict(response.headers)
            self.cookies = response.cookies
            if self.url.startswith('http://') and response.url.startswith("https://"):
                self.url = self.url.replace('http://', 'https://')
            elif self.url.startswith('https://') and response.url.startswith("http://"):
                self.url = self.url.replace('https://', "http://")
            try:
                self.encoding = response.apparent_encoding
            except:
                self.encoding = chardet.detect(self.html)['encoding']

            try:
                self.html = self.html.decode(self.encoding)
            except:
                pass

            # self.domain = null 无法通过ip反查域名（单机情况下）
            # 保留历史响应头信息
            if response.history:
                for history in response.history:
                    # 这里很奇怪，字典update必须单独为一行，不能有其他操作
                    tmp = self.headers
                    self.headers = dict(history.headers)
                    self.headers.update(tmp)

    def do_parse_html(self):
        """
        Parse the HTML with BeautifulSoup to find <script> and <meta> tags.
        进入这个函数意味着后续要对这个webpage进行分析python方式的解析，而不是原生方式
        :return:
        """
        self.soup = BeautifulSoup(self.html, 'lxml')
        self.title = self.soup.title.string if self.soup.title else ''
        self.scripts = [script['src'] for script in
                        self.soup.findAll('script', src=True)]
        self.meta = {
            meta['name'].lower():
                meta['content'] for meta in self.soup.findAll(
                'meta', attrs=dict(name=True, content=True))
        }
        # self.js = ''
        # for url_ in self.scripts:
        #     url_ = self.url + '/' + url_ if 'http' not in url_ else url_
        #     try:
        #         response = self.s.get(url_, timeout=2)
        #         self.js += response.content.decode('utf-8')
        #     except:
        #         pass

    def https_to_http(self):
        if 'https://' in self.url:
            self.url = self.url.replace('https://', 'http://')

    def http_to_https(self):
        if 'http://' in self.url:
            self.url = self.url.replace('http://', 'https://')
