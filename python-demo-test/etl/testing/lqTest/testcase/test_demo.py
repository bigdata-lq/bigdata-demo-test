import unittest
from etl.testing.lqTest.libs.ddt import ddt,data
test_data = [{"xiaoming","${var}","xiaowang","${var}"},{"Content-Type":"application/x-www-form-urlencoded","token":"${houtai_token}"}]

@ddt
class TestDemo(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_data={}

    # @unittest.skip
    @data(("xiaoming","$var"),("xiaowang","$var"))
    def test_01(self,v):
        username, token = v
        print(v)
        print(username,token)
        if token.startswith('$'):
            token = token[1:]
            # 更新变量值
            self.test_data.__setitem__(token,username)
            print(self.test_data)
            # 获取token 的值
        t = self.test_data.get(token)
        print("动态获取变量最新token：", t)
        print(self.test_data)

    # @data(*test_data)
    # def test_02(self,item):
    #     print(item)
    #     if item.startswith('$'):
    #         item = item[1:]
    #         # 更新变量值
    #         self.test_data.__setitem__(item,item)
    #         print(self.test_data)
    #         # 获取token 的值
    #     t = self.test_data.get(item)
    #     print("动态获取变量最新token：", t)
    #     print(self.test_data)




import warnings
from etl.testing.lqTest.tools.httprequest import HttpRequest
import unittest
import gc
import ast
import json
from etl.testing.lqTest.tools.do_database import db,run_mysql
from etl.testing.lqTest.tools.get_global_data import GetData
from etl.testing.lqTest.libs.ddt import ddt,data    #列表嵌套字典、列表嵌套列表
from etl.testing.lqTest.tools.do_excel_xk import DoExcel           #########################################do_excel_xk换成do_excel
from etl.testing.lqTest.dataconfig.project_path import *
from etl.testing.lqTest.tools.my_log import MyLog
from etl.testing.lqTest.tools.read_config import ReadConfig
from etl.testing.lqTest.tools.do_regx import DoRegx

my_logger = MyLog()

# do_excel = DoExcel(test_case_data_path,"login")
# test_data = do_excel.get_all_data()
# my_iterator = iter(test_data)



class TestLogin():
    # @classmethod
    def setUpClass1(cls):
        warnings.simplefilter('ignore', ResourceWarning)
        # 修改token过期时间
        run_mysql("""
            UPDATE app_session ase
            SET ase.add_time = 1614557699
        """)

        # 获取用户token
        print(GetData.user_id)
        res = run_mysql("""
            SELECT user_token
            FROM app_session
            WHERE user_id=%d
        """%(GetData.user_id))
        DoExcel(test_case_data_path,"init").write_back(55,2,res[0]["user_token"])

        # 修改用户支付密码
        run_mysql("""
            UPDATE ceshi.users
            SET  pay_password='3d6868c3b428eaa10a179209ed90943c', salt='Qilv'
            WHERE user_id >= 88
        """)

    def setUp1(self):  # 初始化登录
        pass


    # @unittest.skip
    def test_01(self):
        do_excel = DoExcel(test_case_data_path,"login")
        max_row_num = do_excel.get_max_row_num()
        for r in range(2,max_row_num + 1):
            list_row_data = do_excel.get_row_data_xk(r)
            if bool(list_row_data) == True and list_row_data[0] != {} :
                print(list_row_data)
                for i,item in enumerate(list_row_data):
                    my_logger.info("用例{0}--{1}--{2}------开始执行=====================================================================================".format(item["case_id"],item["module"],item["title"]))
                    my_logger.info("url：{0}--请求方法：{1}\n--请求参数：\n{2}\n--请求头：\n{3}".format(item["url"],item["http_method"],item["data"],item["headers"]))
                    if item["http_method"] == "get" or (item["http_method"] == "post" and "application/x-www-form-urlencoded" in item["headers"]) == True:
                        res = HttpRequest.http_request(item["url"],ast.literal_eval(item["data"]),item["http_method"],ast.literal_eval(item["headers"]))
                    else:
                        res = HttpRequest.http_request(item["url"],item["data"].encode('utf-8'),item["http_method"],ast.literal_eval(item["headers"]))
                    print(res.json())
                    try:
                        # self.assertIn(item["expect"], json.dumps(res.json(), indent=2))  # 存在excel里的不是数字就是字符串，请求的返回值是字符串，所以要转型            #indent=2按照缩进格式
                        TestResult = 'Pass'
                        if item["json_path"] != None:
                            DoExcel(test_case_data_path,"init").get_json_path_value_1(res,list_json_path = ast.literal_eval(item["json_path"]))
                        do_excel.write_back(item["case_id"] + 1,int(ReadConfig.get_test_data("result")), str(res.json()))  # res 返回的是字典，要转成字符串才能写进EXCEL\
                    except AssertionError as e:
                        TestResult = 'Fail'
                        my_logger.error("执行用例断言出错：{0}".format(e))
                        do_excel.write_back(item['case_id'] + 1,int(ReadConfig.get_test_data("result")), str(res.json()))  # res 返回的是字典，要转成字符串才能写进EXCEL\
                        raise e
                    finally:
                        do_excel.write_back(item['case_id'] + 1,int(ReadConfig.get_test_data("test_result")), TestResult)
                        my_logger.info("获取到的结果是:{0}".format(res.json()))
                        my_logger.info("用例{0}执行结束".format(item["case_id"]))
                    # return
            else:
                continue


if __name__ == '__main__':
    # t = TestLogin()
    # t.test_01()
    unittest.main()