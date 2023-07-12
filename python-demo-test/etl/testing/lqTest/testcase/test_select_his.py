from etl.testing.lqTest.tools.httprequest import HttpRequest
import unittest
from etl.testing.lqTest.tools.get_global_data import GetData
from etl.testing.lqTest.libs.ddt import ddt,data    #列表嵌套字典、列表嵌套列表
from etl.testing.lqTest.tools.do_excel_xk import DoExcel
from etl.testing.lqTest.dataconfig.project_path import *
from etl.testing.lqTest.tools.my_log import MyLog
from etl.testing.lqTest.tools.read_config import ReadConfig
my_logger = MyLog()

do_excel = DoExcel(test_case_data_path,"login")
test_data = do_excel.get_all_data()

@ddt
class TestSelectHis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    @data(*test_data)
    def test_select_his(self,item):
        # url = 'http://172.16.20.25:82/center/login'
        # data = {"username":"web","password":"123"}
        my_logger.info("用例{0}-{1}{2}------开始执行".format(item["case_id"], item["module"], item["title"]))
        my_logger.info("请求前的COOKIE{}".format(getattr(GetData,"Cookie")))

        #实现接口数据依赖的替换
        # if item["data"].find("{$load_id}")!=-1:
        #     if getattr(GetData,"loan_id") == None:
        #         query_sql = "select max(Id) from loan where MemberID={0}".format(getattr(GetData,"loadn_id"))
        #         load_id = Operationdb().search(query_sql)[0][0]
        #         item["data"] = item["data"].replace("${load_id}",str(load_id))
        #         setattr(GetData,"load_id",load_id)  #利用反射存储结果
        #         my_logger.info(load_id)
        #     else:
        #         item["data"] = item["data"].replace("${load_id}", str(getattr(GetData,"load_id")))   #通过反射拿到loan_id





        res = HttpRequest.http_request(item["url"],eval(item['data']),item["http_method"],getattr(GetData,"Cookie"))



        #带有httponly属性的cookie---从请求头中去cookie，未成功
        # header = res.request.headers
        # if 'Cookie' in header.keys():
        #     Cookie = header["Cookie"]
        #     # print(Cookie)
        #     cl = Cookie.split("=")
        #     # print(Cookie.split("="))
        #     Cookie = {}
        #     Cookie["ASP.NET_SessionId"] = cl[1]
        #     # print(Cookie)
        #     setattr(GetData,"Cookie",Cookie)
        # # self.assertEqual("200",res.json()["code"])
        # print("请求后的COOKIE{}".format(getattr(GetData,"Cookie")))
        # if item["expect"]:
        #     print(res.json())
            # self.assertEqual(item["expect"], res.json()["total"])

        # if res.cookies :#利用反射存储cookie
        #     setattr(GetData,"Cookie",res.cookies)

        try:
            self.assertEqual(item["expect"], res.json()["total"])  # 存在excel里的不是数字就是字符串，请求的返回值是字符串，所以要转型
            TestResult = 'Pass'
        except AssertionError as e:
            TestResult = 'Fail'
            my_logger.error("执行用例出错：{0}".format(e))
            raise e
        finally:#不管对还是错，，finally后面代码都执行
            do_excel.write_back(test_case_data_path, "login", item['case_id'] + 1,
                                 int(ReadConfig.get_test_data("result")),
                                 str(res.json()))  # res 返回的是字典，要转成字符串才能写进EXCEL\
            do_excel.write_back(test_case_data_path, "login", item['case_id'] + 1,
                                 int(ReadConfig.get_test_data("test_result")), TestResult)
            my_logger.info("获取到的结果是:{0}".format(res.json()))
            my_logger.info("用例{0}执行结束".format(item["case_id"]))
            my_logger.info("*" * 40)

    def tearDown(self):
        pass