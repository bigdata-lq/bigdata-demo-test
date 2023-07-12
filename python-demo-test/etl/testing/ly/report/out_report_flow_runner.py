import unittest
import time
import os.path
from etl.testing.ly.libs.HwTestReport import HTMLTestReport
from etl.testing.ly.utils.read_json import ReadJson

initData = ReadJson("init.json").jsonCase

class OutReportFlowRunner(object):
    # 初始化要用到的字符串
    def __init__(self, cases="./", description=u'环境：windows 10'):
        self.cases = cases
        self.des = description

    # 开始测试
    def run(self, fileName, moduleName):
        # 生成report文件夹
        for filename in os.listdir(self.cases):
            if filename == "html":
                break
        else:
            os.mkdir(self.cases + '/html')
        # 获取当前时间
        now = time.strftime("%Y-%m-%d_%H_%M")
        # 报告结果写入html文件
        with open('./html/' + fileName + "_" + now + "_result.html", 'w', encoding='utf-8') as fp:
            # 运行./路径下的TEST.py文件，视自己的情况修改路径
            tests = unittest.defaultTestLoader.discover("../case/", pattern='*{fileName}.py'.format(fileName = fileName), top_level_dir=None)
            runner = HTMLTestReport(stream=fp, title=moduleName, description=self.des)
            runner.run(tests)


if __name__ == '__main__':
    test = OutReportFlowRunner()
    caseList = initData["case_list"]
    for param in caseList:
        test.run(param["test_case_file_name"], param["module_name"])