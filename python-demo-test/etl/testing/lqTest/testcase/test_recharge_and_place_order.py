import warnings
from etl.testing.lqTest.tools.httprequest import HttpRequest
import unittest
from pprint import pprint
import ast
import json
from etl.testing.lqTest.tools.do_database import run_mysql
from etl.testing.lqTest.tools.get_global_data import GetData
from etl.testing.lqTest.libs.ddt import ddt,data
from etl.testing.lqTest.tools.do_excel_xk import DoExcel
from etl.testing.lqTest.dataconfig.project_path import *
from etl.testing.lqTest.tools.my_log import MyLog
from etl.testing.lqTest.tools.read_config import ReadConfig
from etl.testing.lqTest.tools.do_regx import DoRegx
from faker import Faker

f = Faker(locale='zh_CN')
my_logger = MyLog()

# DoExcel(test_case_data_path,"init").write_init_data_by_faker(list_keys_values=[{"key001":f.name()},{"key002":f.name()}])
do_excel = DoExcel(test_case_data_path,"login")
test_data = do_excel.get_all_data()


@ddt
class TestRechargeAndPlaceOrder(unittest.TestCase):
    """
        GOGO充值下单
    """
    @classmethod
    def setUpClass(cls) -> None:
        import urllib3
        urllib3.disable_warnings()
        warnings.simplefilter('ignore', ResourceWarning)
        DoExcel(test_case_data_path,"init").write_init_data_by_faker(list_keys_values=[{"key001":f.name()},{"key002":f.name()}])

        cls.globals = globals()
        cls.globals["houtai_token"] = None; cls.globals["address_id"] = None; cls.globals["order_id"] = None; cls.globals["user_token"] = None; cls.globals["userToken"] = None

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
            WHERE user_id = %d
        """%(GetData.user_id))

        globals()["user_token"] = res[0]["user_token"]

        # 修改用户支付密码
        run_mysql("""
            UPDATE ceshi.users
            SET  pay_password='3d6868c3b428eaa10a179209ed90943c', salt='Qilv'
            WHERE user_id >= 88
        """)

    def setUp(self):  # 初始化登录
        pass

    # @unittest.skip
    @data(*test_data)
    def test_recharge_and_place_order(self,item):
        """
            GOGO充值下单
        :param item:
        :return:
        """
        # 替换数据=====================================================================================================================
        if "$*" in item["headers"] or "$*" in item["data"] or "$*" in item["check_sql"]:
            try:
                item["headers"] = item["headers"].replace("$*{houtai_token}", self.globals["houtai_token"] or "").replace("$*{userToken}", self.globals["userToken"] or "")    # 有则替换，无则不替换
                item["data"] = item["data"].replace("$*{address_id}",str(self.globals["address_id"]) or "").replace("$*{order_id}", str(self.globals["order_id"]) or "").replace("$*{user_token}", self.globals["user_token"] or "")  # 层层替换   替换一次，下边继续替换
                # item["data"] = item["data"].replace("$*{order_id}", globals()["order_id"] or "")      # 层层替换   替换一次，下边继续替换
            except (ValueError,KeyError) as e:
                raise e

        # 替换数据=====================================================================================================================
        my_logger.info("用例{0}--{1}--{2}------开始执行===================================".format(item["case_id"],item["module"],item["title"]))
        my_logger.info("url：{0}--请求方法：{1}--请求参数：{2}--请求头：{3}".format(item["url"],item["http_method"],item["data"],item["headers"]))
        if item["http_method"] == "get" or (item["http_method"] == "post" and "application/x-www-form-urlencoded" in item["headers"]) == True:
            res = HttpRequest.http_request(item["url"],ast.literal_eval(item["data"]),item["http_method"],ast.literal_eval(item["headers"]))
        else:
            res = HttpRequest.http_request(item["url"],item["data"].encode('utf-8'),item["http_method"],ast.literal_eval(item["headers"]))

        pprint(res.json())
        try:
            self.assertIn(item["expect"], json.dumps(res.json()).encode("utf-8").decode("unicode_escape"))  # 存在excel里的不是数字就是字符串，请求的返回值是字符串，所以要转型      json.dumps(res.json()).encode('utf-8').decode('unicode_escape')   unicode转中文
            TestResult = "Pass"
            result = str(json.dumps(res.json()).encode("utf-8") .decode("unicode_escape")).replace("'", '"')
            do_excel.write_back(item['case_id'] + 1,int(ReadConfig.get_test_data("result")), result)

            # 获取动态数据(PS:获取数据设为全局变量后，一定要在 setUpClass 方法中将全局变量初始化一下为None)==============================================================================================================
            try:
                if item["case_id"] == 1:
                    self.globals["houtai_token"] = DoRegx.get_globals_data(res,"$.data.user_token")  # res.json()["data"]["user_token"]

                elif item["case_id"] == 4:
                    self.globals["address_id"] = DoRegx.get_globals_data(res,"$.data.shipping_address_id")

                elif item["case_id"] == 5:
                    self.globals["order_id"] = DoRegx.get_globals_data(res,"$.data.order_id")


            except KeyError as e:
                print("case_id:%s  ,获取json_path_value失败"%(item["case_id"]))
                my_logger.info("case_id:%s  ,获取动态数据失败%s"%(item["case_id"],e))
            # 获取动态数据==============================================================================================================

            if item["json_path"] != None:
                DoExcel(test_case_data_path,"init").get_json_path_value_1(res,list_json_path = ast.literal_eval(item["json_path"]))
            do_excel.write_back(item["case_id"] + 1,int(ReadConfig.get_test_data("result")), str(res.json()))  # res 返回的是字典，要转成字符串才能写进EXCEL\

        except AssertionError as e:
            TestResult = "Fail"
            my_logger.error("执行用例断言出错：{0}".format(e))
            result = str(json.dumps(res.json()).encode("utf-8").decode("unicode_escape")).replace("'", '"')
            do_excel.write_back(item['case_id'] + 1,int(ReadConfig.get_test_data("result")), result)  # res 返回的是字典，要转成字符串才能写进EXCEL\
            raise e
        finally: # 不管对还是错，，finally后面代码都执行
            # do_excel.write_back(test_case_data_path,"login",item['case_id']+1,int(ReadConfig.get_test_data("result")),str(res.json())) #res 返回的是字典，要转成字符串才能写进EXCEL\
            # do_excel.write_back(test_case_data_path, "login", item['case_id']+1, int(ReadConfig.get_test_data("test_result")),TestResult)
            do_excel.write_back(item['case_id'] + 1,int(ReadConfig.get_test_data("test_result")), TestResult)
            my_logger.info("获取到的结果是:{0}".format(res.json()))
            my_logger.info("用例{0}执行结束\n\n".format(item["case_id"]))


    def tearDown(self):
        pass




if __name__ == '__main__':
    unittest.main()