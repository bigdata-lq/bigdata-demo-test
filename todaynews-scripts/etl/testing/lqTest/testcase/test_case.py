import warnings
from etl.testing.lqTest.tools.httprequest import HttpRequest
import unittest
import ast
import json,chardet
from etl.testing.lqTest.tools.do_database import run_mysql
from etl.testing.lqTest.tools.get_global_data import GetData
from etl.testing.lqTest.libs.ddt import ddt,data
from etl.testing.lqTest.tools.do_excel_xk import DoExcel           #########################################do_excel_xk换成do_excel
from etl.testing.lqTest.dataconfig.project_path import *
from etl.testing.lqTest.tools.my_log import MyLog
from etl.testing.lqTest.tools.do_regx import DoRegx
from etl.testing.lqTest.tools.read_config import ReadConfig


my_logger = MyLog()

do_excel = DoExcel(test_case_data_path,"login")
# print(do_excel)
test_data = do_excel.get_all_data()
# print(test_data)


@ddt
class TestMMTRechargeAndPlaceOrder(unittest.TestCase):#unittest.TestCase  父类
    """
        MMT充值下单
    """
    @classmethod
    def setUpClass(cls) -> None:
        import urllib3
        urllib3.disable_warnings()
        warnings.simplefilter('ignore', ResourceWarning)
        cls.globals = globals()
        cls.globals["houtai_token"] = None; cls.globals["address_id"] = None; cls.globals["user_token"] = None; cls.globals["cart_id"] = None; cls.globals["order_id"] = None


    def setUp(self):
        pass

    # @unittest.skip
    @data(*test_data)
    def test_MMT_recharge_and_place_order(self,item):
        """
            MMT充值下单
        :param item:
        :return:
        """
        # 替换数据====（数据一条一条替换）=================================================================================================================

        if "$*" in item["headers"] or "$*" in item["data"]:
            try:
                # print("替换前：",item["headers"])
                # print("替换前：",item["data"])
                item["headers"] = item["headers"].replace("$*{houtai_token}", str(self.globals["houtai_token"]) or "").replace("$*{user_token}", str(self.globals["user_token"]) or "")   # 有则替换，无则不替换
                item["data"] = item["data"].replace("$*{address_id}",str(self.globals["address_id"]) or "").replace("$*{order_id}",str(self.globals["order_id"]) or "").replace("$*{user_token}", str(self.globals["user_token"]) or "").replace\
                                            ("$*{cart_id}", str(self.globals["cart_id"]) or "") # 层层替换   替换一次，下边继续替换
                # print("替换后：",item["headers"])
                # print("替换后：",item["data"])
            except (ValueError,KeyError) as e:
                raise e

        my_logger.info("用例{0}--{1}--{2}------开始执行===================================".format(item["case_id"],item["module"],item["title"]))
        my_logger.info("url：{0}--请求方法：{1}--请求参数：{2}--请求头：{3}".format(item["url"],item["http_method"],item["data"],item["headers"]))

         #ast.literal_eval 数据类型的相互转换（eval既可以做string与list,tuple,dict之间的类型转换）
        if item["http_method"] == "get" or (item["http_method"] == "post" and "application/x-www-form-urlencoded" in item["headers"]) == True:
            res = HttpRequest.http_request(item["url"],ast.literal_eval(item["data"]),item["http_method"],ast.literal_eval(item["headers"]))
        else:
            res = HttpRequest.http_request(item["url"],item["data"].encode('utf-8'),item["http_method"],ast.literal_eval(item["headers"]))
        # print(111111111111111111111111111111,chardet.detect(res))
         #dumps 序列化 字典{}转换成字典字符串（'{}'） 、loads 反序列化 字典字符串（'{}'） 转换成字典{}  json数据
        try:
            self.assertIn(item["expect"], json.dumps(res.json()).encode("utf-8").decode("unicode_escape"))  # 存在excel里的不是数字就是字符串，请求的返回值是字符串      json.dumps(res.json()).encode('utf-8').decode('unicode_escape')   unicode转中文
            TestResult = "Pass"
            result = str(json.dumps(res.json()).encode("utf-8") .decode("unicode_escape")).replace("'", '"')
            do_excel.write_back(item['case_id'] + 1,int(ReadConfig.get_test_data("result")), result)


            # 获取动态数据(PS:获取数据后设为 1、全局变量后，2、一定要在 setUpClass 方法中将全局变量初始化一下为None)====拿到后将token存入全局变量==========================================================================================================
            try:
                if item["case_id"] ==19:
                    self.globals["user_token"] = DoRegx.get_globals_data(res,"$.data.userToken")

                elif item["case_id"] == 21:
                    self.globals["address_id"] = DoRegx.get_globals_data(res,"$.data.addressId")

                elif item["case_id"] == 23:
                    self.globals["cart_id"] = DoRegx.get_globals_data(res,"$.data.data.cart_id")#result(返回结果参数化)

                elif item["case_id"] == 24:
                    self.globals["order_id"] = DoRegx.get_globals_data(res,"$.data.orderId")

            except KeyError as e:
                print("case_id:%s  ,获取json_path_value失败,报错信息：%s"%(item["case_id"],e))
                my_logger.info("case_id:%s  ,获取动态数据失败%s"%(item["case_id"],e))
                raise e
            # 获取动态数据(先断言再获取到动态数据)==============================================================================================================

        except AssertionError as e:
            TestResult = "Fail"
            my_logger.error("执行用例断言出错：{0}".format(e))
            result = str(json.dumps(res.json()).encode("utf-8").decode("unicode_escape")).replace("'", '"')
            do_excel.write_back(item['case_id'] + 1,int(ReadConfig.get_test_data("result")), result)  # res 返回的是字典，要转成字符串才能写进EXCEL\
            raise e
        finally: # 不管对还是错，，finally后面代码都执行
            do_excel.write_back(item['case_id'] + 1,int(ReadConfig.get_test_data("test_result")), TestResult)
            my_logger.info("获取到的结果是:{0}".format(res.json()))
            my_logger.info("用例{0}执行结束\n\n".format(item["case_id"]))


    def tearDown(self):
        pass



if __name__ == '__main__':
    unittest.main()


