import os
import re
import functools
from concurrent.futures import ThreadPoolExecutor
from yuantool.url import format_url


# Static methods


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


def get_orignal_url(item):
    tmp = sorted(item['urls'])
    return format_url(tmp[0])


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
                returned = list(tqdm.tqdm(ThreadPoolExecutor(max_workers=workers).map(func, elements), **tqdm_args))
            else:
                returned = list(ThreadPoolExecutor(max_workers=workers).map(func, elements))
        else:
            raise AttributeError('When asynch == True : You must specify a integer value for workers')
    else:
        if progress:
            elements = tqdm.tqdm(elements, **tqdm_args)
        for index_or_item in elements:
            returned.append(func(index_or_item))
    return returned