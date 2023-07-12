import requests
from etl.testing.lqTest.dataconfig.project_path import *
#MyLog 类方法
from etl.testing.lqTest.tools.my_log import MyLog
my_logger = MyLog()


class HttpRequest:

    @staticmethod #静态方法
    def http_request(url,data,http_method,headers = None,verify = False):
        try:
            #upper() 方法作用：小写转换成大写  try "假如不是post、get请求，else 报错"  except Exception "报错原因"
            if http_method.upper() == 'GET':
                res = requests.get(url,data,headers = headers,verify = verify)
            elif http_method.upper() == "POST":
                res = requests.post(url,data,headers = headers,verify = verify)
            else:
                # info 方法把错误信息写到文本日志
                my_logger.info("请求方法错误")
            # return res   #返回消息实体（从函数返回计算结果）

        except Exception as e:
            my_logger.error("请求报错了：{0}".format(e))
            raise e
            # raise 异常抛出操作   把e的异常抛出
        return res   #返回消息实体（从函数返回计算结果）


if __name__ == '__main__':
    hr = HttpRequest()
    # url = 'http://172.16.20.25:82/center/login'
    # data ={"username":"web","password":"123"}
    # res = hr.http_request(url,data,"post")
    # print(res.json())
    #
    #
    # res =  hr.http_request(
    #           url="https://shop.uat.zgmmtuan.com/rapi/coupon/available",
    #           data={
    #               "product_id":'["29411","29403"]',
    #               "pageSize":10,
    #               "pagNum":1
    #           },
    #           http_method="post",
    #           headers = {
    #               "userToken":"d624e52d2cabfa5f68a90c7912014723",
    #               "Content-Type":"application/x-www-form-urlencoded",
    #               # "platform":"android"
    #           }
    # )
    # print(res.json())