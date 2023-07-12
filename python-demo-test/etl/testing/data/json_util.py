import json


def dumpJson(path):
    """
    读取json文件数据
    :param path:
    :return:
    """
    with open(path,'r',encoding='utf8')as fp:
        json_data = json.load(fp)
    return json_data


if __name__ == '__main__':
    json_data = dumpJson("./extendedConfig.json")
    print('这是文件中的json数据：',json_data)
    print('这是读取到文件数据的数据类型：', type(json_data))