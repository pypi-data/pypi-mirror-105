import os
import json
import requests
from pathlib import Path
from yuantool.path import abs_find_program as where_is


class Technologies:
    """
    对指纹文件的一系列操作
    """

    project_file = Path(__file__).parent.joinpath('data').joinpath('technologies.json')
    sys_file = Path(where_is('wappalyzer')).parent.joinpath('technologies.json') if where_is('wappalyzer') else None
    cus_file = Path(__file__).parent.joinpath('data').joinpath('technologies_cus.json')
    bak_file = Path(__file__).parent.joinpath('data').joinpath('technologies_bak.json')
    latest_file = Path(__file__).parent.joinpath('data').joinpath('latest_technologies.json')

    @classmethod
    def get_latest_technologies_file(cls):
        """
        从github上获取最新的指纹内容
        1、将先去github上获取新的指纹
        2、运行检查新文件是否可以被json化读取（因为经常会更新有问题的文件）
        3、若可以则使用新文件，若不行则使用可使用版本的文件，
        :return: 升级是否成功
        """
        try:
            latest_technologies_file = requests.get(
                'https://raw.githubusercontent.com/AliasIO/wappalyzer/master/src/technologies.json')
        except:
            print("从github上获取新指纹文件失败")
            return False
        cls.write_file(cls.latest_file, latest_technologies_file.text)
        try:
            obj = cls.read_json_file(cls.latest_file)
        except:
            os.remove(cls.latest_file)
            print("新文件无法正确读取，已经删除")
            return False
        try:
            os.remove(cls.bak_file)
        except Exception:
            pass
        os.rename(src=cls.project_file, dst=cls.bak_file)
        os.rename(src=cls.latest_file, dst=cls.project_file)
        return True

    @classmethod
    def _combine(cls, enforce: bool = False):
        """
        将网上指纹信息与本地指纹信息整合形成新的指纹文件
        :param enforce: 遇到重复指纹是否替换，默认不替换,True则替换
        :return:
        """
        project_data = cls.read_json_file(cls.project_file)

        cus_data = cls.read_json_file(cls.cus_file)

        if not enforce:
            for item in cus_data['technologies']:
                if item not in project_data['technologies']:
                    project_data['technologies'][item] = cus_data['technologies'][item]
        else:
            project_data['technologies'].update(cus_data['technologies'])

        cls.write_file(cls.project_file, json.dumps(project_data))

    @classmethod
    def _copy_2_sys_file(cls):
        if cls.sys_file:
            project_data = cls.read_file(cls.project_file)
            cls.write_file(cls.sys_file, project_data)

    @staticmethod
    def read_file(path):
        with open(path, 'r', encoding='utf-8') as f:
            res = f.read()
        return res

    @staticmethod
    def write_file(path, data):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(data)

    @staticmethod
    def read_json_file(path):
        return json.loads(Technologies.read_file(path))

    @staticmethod
    def write_json_file(path, data):
        Technologies.write_file(path, json.dumps(data, ensure_ascii=False))


if __name__ == '__main__':
    print(Technologies.project_file)
    print(Technologies.sys_file)
