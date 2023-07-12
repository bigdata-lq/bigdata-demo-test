#测试数据路径,配置文件路径,用例执行控制路径,测试用例路径,测试报告路径,日志输出路径
#os系统对象
import os
import time

#1、获取到APItest_unittest_cmp-master，以找到其他路径做前提

#获取脚本所在路径 （获取py脚本所在路径）
a = os.path.realpath(__file__)#含脚本


#使用os.path.split()分割路径与文件，以元组（）的形式返回，我们运用这个特性获取py文件的上级路径‘scrip
b = os.path.split(os.path.realpath(__file__))[0] #不含脚本（当前所在路径） [0]== . 上一级   [0][0]== .. 上两级


 #读取位置 (进入到框架位置的路径“APItest_unittest_cmp-master”)
project_path = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

#2、在APItest_unittest_cmp-master路径的前提下找到要的其他路径  (os.path.join 用于路径的拼接）

# #测试数据路径 (os.path.join 用于路径的拼接）
test_case_data_path = os.path.join(project_path,"test_data","case - 副本 - 副本2.xlsx")
# print(test_case_data_path)
#
#配置文件路径
config_path = os.path.join(project_path,"dataconfig","config.ini")

#用例执行控制路径（控制哪些用例可以执行）
caseList_path = os.path.join(project_path,"dataconfig","caselist.txt")

#测试用例路径    (os.path.join 用于路径的拼接）

test_case_path = os.path.join(project_path,"testcase")

#
# #测试报告路径
now = time.strftime("%Y-%m-%d %H-%M-%S") #当地时间
report_path = os.path.join(project_path,"test_result","html_report",now+"-"+"api_test.html")
#
# #日志输出路径
log_path = os.path.join(project_path,"test_result","log","runlog.log")
#
#
if __name__ == '__main__':
    print(a)
    print(b)
    print(project_path)
    print(report_path)
    print(config_path)
    print(log_path)
    print(caseList_path)
    print(test_case_path)
    print(test_case_data_path)