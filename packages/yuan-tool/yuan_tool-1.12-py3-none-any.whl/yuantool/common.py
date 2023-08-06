import platform
import string
import os
import sys
import re
import random


def check_keys(require_keys, request_keys):
    flag = True
    lost_key = None
    for key in require_keys:
        if not (key in request_keys.keys() and request_keys[key]):
            flag = False
            lost_key = key
    return flag, lost_key


def getattr_value(arr, key):
    return getattr(arr, key) if key in arr else ''


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


def random_str(length=10, chars=string.ascii_lowercase):
    return ''.join(random.sample(chars, length))
