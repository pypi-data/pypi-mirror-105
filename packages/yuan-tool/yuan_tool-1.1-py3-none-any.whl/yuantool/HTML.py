import re
import requests
import json

import logging

logger = logging.getLogger(__name__)


class Success:
    code = 'code'
    msg = 'msg'
    data = 'data'
    Success = {code: 0, msg: 'success', data: []}
    TASK_START = {code: 0, msg: 'task in progress'}


# from fake_useragent import UserAgent


session = requests.Session()
session.keep_alive = False


# ua = UserAgent()


def get_html(url):
    # change_user_agent()
    html = session.get(url)
    if html.status_code == 200:
        res = html.text
    else:
        res = False
    return res


def put_data(url, data):
    try:
        flag = True

        if len(data) == 1:
            pass
            # logger.info(f'{target}没有web资产，不发送数量信息')
        else:
            html = session.post(url, data=json.dumps(data))
            if html.status_code == 200:
                logger.debug('向url:{} 发送数据成功,内容为{}'.format(url, data))
                # continue
            else:
                flag = False
        if flag:
            res = True
        else:
            res = False
    except Exception as e:
        if 'Failed to establish a new connection:' in str(e):
            logger.warning(e)
        else:
            logger.warning(e, exc_info=True)
        res = False
    return res


def put_full_data(url, data):
    res = True
    try:
        data = dict(enumerate(data))
        html = session.post(url, json=data)
        if html.status_code == 200:
            logger.debug('向url:{} 发送数据成功,内容为{}'.format(url, data))
        else:
            res = False
    except Exception as e:
        if 'Failed to establish a new connection:' in str(e):
            logger.warning(e)
        else:
            logger.warning(e, exc_info=True)
        res = False
    return res


def put_divide_data(url, data):
    try:
        flag = True
        for res in data:
            html = session.post(url, json=res)
            if html.status_code == 200:
                continue
            else:
                flag = False
        if flag and data:
            logger.debug('向url:{} 发送数据成功,内容为{}'.format(url, data))
            res = True
        else:
            res = False
    except Exception as e:
        if 'Failed to establish a new connection:' in str(e):
            logger.warning(e)
        else:
            logger.warning(e, exc_info=1)
        res = False
    return res


def post(url):
    try:
        res = session.post(url)
        if res.status_code != 200:
            res = False
    except Exception as e:
        if 'Failed to establish a new connection:' in str(e):
            logger.warning(e)
        else:
            logger.warning(e, exc_info=True)
        res = False
    return res


def post_data(url, data):
    # change_user_agent()
    try:
        res = session.post(url, data=str(data).encode('utf-8'))
        if res.status_code != 200:
            res = False
    except Exception as e:
        if 'Failed to establish a new connection:' in str(e):
            logger.warning(e)
        else:
            logger.warning(e, exc_info=1)
        res = False
    return res


def post_task_status(url, task):
    try:
        res = Success.TASK_START
        ips = str(task.ip).replace('，', ',').split(',')
        for ip in ips:
            res['ip'] = ip
            # res = dict2str(res)
            html = session.post(url=url, data=res, timeout=10)
            if html.status_code != 200:
                res = False
    except Exception as e:
        if 'Failed to establish a new connection:' in str(e):
            logger.warning(e)
        else:
            logger.warning(e, exc_info=True)
        res = False
    return res

# def change_user_agent():
#     session.headers['User-Agent'] = ua.random
#     session.headers['X-forwarded-for'] = '49.49.49.49'
