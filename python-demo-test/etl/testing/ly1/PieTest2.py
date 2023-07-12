import unittest
from etl.testing.ly1.HwTestReport import HTMLTestReport
from etl.testing.ly1.TEST import TestMethods



if __name__ == '__main__':

    # 初始化测试上下文
    suite = unittest.TestSuite()
    # suite.addTest(unittest.makeSuite(ExtendedTest))
    suite.addTest(TestMethods("test_pass"))
    suite.addTest(TestMethods("test_failed"))
    suite.addTest(TestMethods("test_error"))
    # 存放路径在E盘目录下
    filepath='./pyresult.html'
    fp=open(filepath,'wb')
    #定义测试报告的标题与描述
    runner = HTMLTestReport(stream=fp,title=u'扩展字段自动化测试报告',description=u'扩展字段功能自动化测试')
    runner.run(suite)
    fp.close()