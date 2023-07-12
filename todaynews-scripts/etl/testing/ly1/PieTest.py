import unittest
import time
import os.path
from etl.testing.ly1.HwTestReport import HTMLTestReport

class TestRunner(object):
    # 初始化要用到的字符串
    def __init__(self, cases="./", title=u'自动化测试报告', description=u'环境：windows 10'):
        self.cases = cases
        self.title = title
        self.des = description

    # 开始测试
    def run(self):
        # 生成report文件夹
        for filename in os.listdir(self.cases):
            if filename == "report":
                break
        else:
            os.mkdir(self.cases + '/report')
        # 获取当前时间
        now = time.strftime("%Y-%m-%d_%H_%M_%S")
        # 报告结果写入html文件
        with open('./report/' + now + "_result.html", 'w', encoding='utf-8') as fp:
            # 运行./路径下的TEST.py文件，视自己的情况修改路径
            tests = unittest.defaultTestLoader.discover("./", pattern='*TEST.py', top_level_dir=None)
            runner = HTMLTestReport(stream=fp, title=self.title, description=self.des)
            runner.run(tests)


if __name__ == '__main__':
    test = TestRunner()
    test.run()