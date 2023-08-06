import base64
import hashlib
from urllib import parse

''' 对外用户开放的方法 '''


def urlEncode(s) -> str:
    return parse.quote(s)


def urlDecode(s) -> str:
    return parse.unquote(s)


def md5(s, salt='') -> str:
    s = str(s)
    strs = (s + salt).encode('utf-8')
    return hashlib.md5(strs).hexdigest()


def base64Encode(s) -> bytes:
    s = str(s)
    return base64.b64encode(s.encode('utf-8'))


def base64Decode(s) -> str:
    s = str(s)
    return base64.b64decode(s).decode('utf-8')


def json_to_str(s) -> str:
    ''' 表单转字符串 '''
    return parse.urlencode(s)
