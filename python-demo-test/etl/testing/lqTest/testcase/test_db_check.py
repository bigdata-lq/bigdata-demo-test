import unittest
from etl.testing.lqTest.tools.httprequest import HttpRequest
from etl.testing.lqTest.tools.get_global_data import GetData
from etl.testing.lqTest.libs.ddt import ddt,data  #列表嵌套列表或者列表嵌套字典适合用ddt
from etl.testing.lqTest.tools.do_excel_xk import DoExcel
from etl.testing.lqTest.dataconfig.project_path import *
from etl.testing.lqTest.tools.do_database import DoDatabase
from etl.testing.lqTest.tools.my_log import MyLog
from etl.testing.lqTest.tools.read_config import ReadConfig


#校验充值前余额和充值后余额（不是所有的用例都要做校验，所以用一个checklist把要做数据库校验的放进去）

        #数据库校验   请求前和请求后

        # if item["sheet_name"] in getattr(GetData,"check_list"):
        #     #sql查询请求之前的余额
        #     #查询数据库
        #
        #     query_sql = "select LeaveAmount from member where MobilePhone={0}".format(eval(item["data"])["mobilephone"])
        #     Before_Amount = DoDatabase().search(query_sql,1)[0]
        #
        #     res = Http_Request.http_request(item["url"], eval(item["data"]), item["http_method"], getattr(GetData, "Cookie"))
        #     # sql查询请求之后的余额
        #     query_sql = "select LeaveAmount from member where MobilePhone={0}".format(eval(item["data"])["mobilephone"])
        #     After_Amount = DoDatabase().search(query_sql, 1)[0]
        #
        #     if abs(Before_Amount-After_Amount) == eval(item["data"]["Amount"]):
        #         check_res = '金额正确'
        #     else:
        #         check_res = "金额错误"

            #1:并不是所有的用例都要做检查，是否要做数据库校验可以在excel里增加一个列，如果里面有{"sql"：""}就执行，没有为NONE则不执行
            #2：怎么把数据库检查结果写到excel里
            #3：多个sql语句     ---列表嵌套字典



# test_data = DoExcel.get_data(r"F:\接口测试框架\NMB_API\test_data\test_data.xlsx","login")
test_data = DoExcel.get_data(test_case_path,"login")

@ddt
class TestHttpRequest(unittest.TestCase):
    def setUp(self):
        pass

    @data(*test_data)
    def test_api(self,item):
        my_logger = MyLog()

        my_logger.info("用例{0}-{1}{2}------开始执行".format(item["case_id"], item["module"], item["title"]))
        #loan_id的替换
        if item["data"].find("{$loan_id}")!=-1:
            if getattr(GetData,"loan_id") == None:
                query_sql = "select max(Id) from loan where MemberID={0}".format(getattr(GetData,"loadn_id"))
                load_id = DoDatabase().search(query_sql)[0][0]
                item["data"] = item["data"].replace("${load_id}",str(load_id))
                setattr(GetData,"load_id",load_id)
                my_logger.info(load_id)
            else:
                item["data"] = item["data"].replace("${load_id}", str(getattr(GetData,"load_id")))

        my_logger.info("获取到的请求数据是{0}".format(item["data"]))
        if item["check_sql"]!=None:#  当你的check——sql语句不为空的时候，就可以进行数据库校验
            my_logger.info("此条用例需要做数据库校验{0}".format(item["title"]))
            query_sql = eval(item["check_sql"])["sql"]
            #开始查询
            # 请求之前账户的余额
            Before_Amount = DoDatabase.search(query_sql,1)[0]
            my_logger.info("用例：{0}请求之前的余额是：{1}".format(item["title"],Before_Amount))

            #自己检查，这里数据的金额格式是两位小数，是否会有问题，数据库中存储的类型！！！！
            my_logger.info("----------------开始HTTP请求----------------")
            res = HttpRequest.http_request(item["url"], eval(item["data"]), item["http_method"],
                                            getattr(GetData, "Cookie"))
            my_logger.info("---------------完成HTTP请求----------------")
            ##请求之后账户的余额
            After_Amount = DoDatabase.search(query_sql,1)[0]
            my_logger.info("用例：{0}请求之后的余额是：{1}".format(item["title"], After_Amount))

            #检查结果、
            if eval(item["data"])["mount"] == abs(After_Amount-Before_Amount):
                my_logger.info("数据库余额校验通过")
                check_sql_result = "数据库检查通过"
            else:
                my_logger.info("数据库余额校验不通过")
                check_sql_result = "数据库检查不通过"

            #怎么把结果写进去
            DoExcel.write_back(test_case_path,item["sheet_name"],item["case_id"]+1,12,check_sql_result)


        else:
            my_logger.info("此条用例不做数据库校验{0}".format(item["title"]))
            my_logger.info("----------------开始HTTP请求----------------")
            res = HttpRequest.http_request(item["url"], eval(item["data"]), item["http_method"],
                                            getattr(GetData, "Cookie"))
            my_logger.info("---------------完成HTTP请求----------------")


        # 利用反射存储cookie
        if res.cookies :
            setattr(GetData,"Cookie",res.cookies)
#断言
        # self.assertEqual("10001",res.json()["code"])
        try:
            self.assertEqual(str(item["expected"]),res.json()["code"])  # 存在excel里的不是数字就是字符串，请求的返回值是字符串，所以要转型
            TestResult = 'Pass'
        except AssertionError as e:
            TestResult = 'Fail'
            print("执行用例出错：{0}".format(e))
            raise e
        finally:#不管对还是错，，finally后面代码都执行
            DoExcel().write_back(test_case_data_path, "login", item['case_id'] + 1,
                                 int(ReadConfig.get_test_data("result")),
                                 str(res.json()))  # res 返回的是字典，要转成字符串才能写进EXCEL\
            DoExcel().write_back(test_case_data_path, "login", item['case_id'] + 1,
                                 int(ReadConfig.get_test_data("test_result")), TestResult)
            print("获取到的结果是:{0}".format(res.json()))


    def tearDown(self):
        pass