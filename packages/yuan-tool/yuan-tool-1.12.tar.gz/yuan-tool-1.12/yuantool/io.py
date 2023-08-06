import yaml


def read_file(file, encoding='utf-8'):
    """
    :param file: 文件名
    :param encoding: 编码，默认utf-8
    :return:
    """
    with open(file, 'r', encoding=encoding) as f:
        return f.read()


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
