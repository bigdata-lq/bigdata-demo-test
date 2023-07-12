#导包 json
import json

class ReadJson(object):

    def __init__(self,filename):
        self.filepath = "../data/"+ filename
        self.jsonCase = self.read_json()

    def read_json(self):
        with open(self.filepath, "r", encoding="utf-8")as f:
             return json.load(f)

    ##根据类型获取单条用例
    def getCaseByType(self, type):
        case = self.jsonCase.get(type)
        # 新建空列表，添加读取json数据
        caseArr = []
        caseArr.append((case.get("url"),
                     case.get("param"),
                     case.get("expect_result"),
                     case.get("status_code"), case.get("name")))
        return caseArr


if __name__ == '__main__':

    print(ReadJson("money_flow.json").getCaseByType(type = "jj_001"))

    json = ReadJson("money_flow_1.json")
    print(type(json.jsonCase))

    print(json.jsonCase)

