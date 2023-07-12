#导包 json
import json

#打开json文件并获取文件流
#with open ("../data/login.json","r",encoding="utf-8")as f:
    # 调用load方法加载文件流
  #  data =json.load(f)
  #  print("获取数据为：",data)
#def read_json():
 #   with open("../data/login.json", "r", encoding="utf-8")as f:
#          return json.load(f)
#
class ReadJson(object):
    def __init__(self,filename):
        self.filepath = "../data/"+ filename
    def read_json(self):
        with open(self.filepath, "r", encoding="utf-8")as f:
             return json.load(f)

if __name__ == '__main__':

    data = ReadJson("login.json").read_json()
    data = data["app_pankoService_historicalTrend"]
    arrs = []
    arrs.append((data.get("url"),
               data.get("param"),
               data.get("expect_result"),
               data.get("status_code")))
    print(arrs)

