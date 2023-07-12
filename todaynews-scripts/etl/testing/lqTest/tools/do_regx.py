import re #re正则表达式（包）
from etl.testing.lqTest.tools.get_global_data import GetData#读取数据  (测试用的数据)
from etl.testing.lqTest.tools.read_config import ReadConfig#读配置文件 (配置数据)
from jsonpath import jsonpath

# s = "www.lefix.com"  #目标字符串
# res = re.match("(w)(ww).*",s)  #全匹配   头部匹配  只匹配一次
# print(res)
# print(res.group())  #分组 根据括号里的正则表达式去分组   group() == group(0)  拿到匹配的全字符
# print(res.group(1))    #（）就是分组，group（1）就是拿第一个括号里的内容
# print(res.group(2))
#
# res = re.findall('(le)(fix)',s)  #返回的是列表
# #如果有分组，就是以元祖的形式表现，列表嵌套元祖
# print(res)
#
# #替换一个
# s = '{"username":"${user}","password":"passwd"}'    #字符串
#
# #search  每次只匹配一个
# res = re.search('\$\{(.*)\}',s)
# print(res)
# print(res.group(),"dddddddddddddddddddd")
#
# res = re.search('\$\{(.*?)\}',s)   # .*？  匹配到第一个就停止       （）就是分组，group（1）就是拿第一个括号里的内容
# print(res)
# key = (res.group(0))
# value = (res.group(1))
# print(key,value,"oooooooooooooooooooooo")
# new_s = s.replace(key,str(getattr(GetData,"admin_user")))
# print(new_s)



PATTERN = eval(ReadConfig.get_regx())  #eval函数就是实现list、dict、tuple与str之间的转化 (表达式字符串转换成字典格式)
# '{}'=eval()  >--- {}
# print(PATTERN,1111111111111111111111111111111)


class DoRegx:
#替换包多个字符串

    @staticmethod #静态方法
    def do_regx(s:str):
        #search  每次只匹配一个
        # while re.search('\$\{(.*?)\}',s):
        #     key =re.search('\$\{(.*?)\}',s).group(0)
        #     value = re.search('\$\{(.*?)\}',s).group(1)
        #     s = s.replace(key,str(getattr(GetData,value)))
        #a = re.findall("匹配规则"(PATTERN), "要匹配的字符串"s字符串") #第二步，调用模块函数
        res = re.findall(PATTERN,s) #re.findall  的简单用法（返回string中所有与pattern相匹配的全部字符串，返回形式为数组
                                    #re findall 方法能够以列表的形式返回能匹配的子字符串
        # print("res:",res)
        for item in range(len(res)):#item 下标   len(res)：元素的总数 循环去替换成值
            s = s.replace("${" + res[item] + "}", str(getattr(GetData, res[item]))) #getattr 获取键的值   PATTERN:正则表达式
            # print(str(getattr(GetData, res[item])))                           # 也可以把要替换的数据写到config中，这里就换成读取配置文件的写法   res[item]==['url']
                                        #${" + res[item] + "}===key , str(getattr(GetData, res[item]))====value  '''字符串'''  item 下标
        return s

    @staticmethod
    def get_globals_data(res,json_path:str):
        json_path_value = jsonpath(res.json(),json_path) #json_path路径
        if json_path_value != False:         # 若获取json_path_value值失败会返回 False  列表
            print("获取到 (%s) 的json_path_value为：=====>>>    %s"%(json_path,str(json_path_value[0])))
            return json_path_value[0]
        else:
            raise KeyError



    @staticmethod
    def replaceFomat(text: str, word: str, n: int,reverse=False):
        '''对文本中的指定单词进行格式化的替换/替回
        Params:
        ---
        text
            要替换的文本
        word
            目标单词
        n
            目标单词的序号
        reverse
            是否进行替回
        Return:
        ---
        new_text
            替换后的文本
        '''
        # 构造【中间变量】
        new_text = text[ : ]
        fmt = "<{}>".format(n)
        # 替换
        if reverse is False:
            new_text = new_text.replace(word, fmt)  # 格式化替换
            return new_text
        # 替回
        elif reverse is True:
            new_text = new_text.replace(fmt, word)  # 去格式化替换
            return new_text
        # 要求非法，引发异常
        else:
            raise TypeError

    @staticmethod
    def replaceMulti(text: str, olds: list, news: list):
        '''一次替换多组字符串
        Params:
        ---
        text
            要替换的文本
        olds
            旧字符串列表
        news
            新字符串列表
        Return:
        ---
        new_text: str
            替换后的文本
        '''
        if len(olds) != len(news):
            raise IndexError
        else:
            new_text = text[ : ]
            # 格式化替换
            i = 0  # 单词计数器
            for word in olds:
                i += 1
                new_text = DoRegx.replaceFomat(new_text, word, i)
            # 去格式化替回
            i = 0  # 归零
            for word in news:
                i += 1
                new_text = DoRegx.replaceFomat(new_text, word, i,True)
            # 返回替换好的文本
            return new_text



def rep(rawstr, dict_rep:dict):
    for i in dict_rep:
        rawstr = rawstr.replace(i, dict_rep[i])
    return rawstr


if __name__ == '__main__':
#     s = '{"loginName":"loginName","password":"passwor","boy":"${how_much_is_a_piece_worth}","xx":"kk"}' 字典字符串
    # s = 'http://${url}/capi/customer/public/login'
    # print(PATTERN)
    # print(DoRegx.do_regx(s))
    #$*{admin_user123}
    aaa = DoRegx.get_globals_data
    print(DoRegx.get_globals_data)



    # import re
    # from tools.get_global_data import GetData
    # PATTERN = '\$\{(.*?)\}'
    # s = '{"username":"${admin_user111}","password":"${admin_passwd111}"}'
    # res = re.findall(PATTERN,s)
    # print(res)
    # print(res[1])
    # print(getattr(GetData,res[1]))
    #
    # for item in range(len(res)):
    #     print(res[item])
    #     s = s.replace("${"+res[item]+"}", str(getattr(GetData, res[item])))
    # print(s)