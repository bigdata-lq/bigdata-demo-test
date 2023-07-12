# pymysql连接python和mysql之间的通道（db(str):        数据库名称）
import pymysql
#连接数据库的类包
import json
#ReadConfig 类名
from etl.testing.lqTest.tools.read_config import ReadConfig
from etl.testing.lqTest.dataconfig.project_path import *
from pprint import pprint
#导入游标对象（开启游标功能执行这个SQL语句后，系统并不会将结果直接打印到频幕上，而是将上述得到的结果，找个地方存储起来，提供一个游标接口给我们，当你需要获取数据 的时候，就可以从中拿数据）
import pymysql.cursors

class DoDatabase:
    def __init__(self):
        ### 测试库  使用pymysql类包中的 Connect 连接方法：连接数据库  ReadConfig.get_mysql_connect：类名+方法名表示取的值
        self.connect = pymysql.Connect(
            host=ReadConfig.get_mysql_connect("host"),
            port=int(ReadConfig.get_mysql_connect("port")),
            user=ReadConfig.get_mysql_connect("user"),
            passwd=ReadConfig.get_mysql_connect("passwd"),
            db=ReadConfig.get_mysql_connect("db"),
            charset=ReadConfig.get_mysql_connect("charset")
        )

        ### 开发库
        # connect = pymysql.Connect(
        #     host="rm-bp1l3z2xvjyds7zv2.mysql.rds.aliyuncs.com",
        #     port=3306,
        #     user="devmmt",
        #     passwd="Bv^Pt!sVfi2fvmSq",
        #     db="dev-mmt-mall",
        #     charset="utf8"
        # )

        # 获取游标,返回值以字典的形式返回
        self.cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)




    def run_mysql(self,sql_words = ""):
        """
            运行sql语句
            :param:  sql_words: sql语句
            :return: 返回查询数据对应的字典列表
        """

        # 定义返回结果列表
        sql_list = []
        #捕获异常
        try:
            # 执行SQL语句（尝试异常语句）（ self.cursor  （游标）方法执行 SQL 查询 ）放一行
            self.cursor.execute(sql_words)
            self.connect.commit()#提交数据库执行（db）
            # .fetchall方法是获取列表所有记录 .fetchall
            results = self.cursor.fetchall()
            # 结果格式处理  （列表的方式输出）（追加写入列表1、先定义列表 sql_list = [] 2、逐行追加写入到列表中）
            for i in results:
                # sql_list.append(copy.deepcopy(i))
                sql_list.append(i)
        except:
            print("Error: 无法获取数据库数据,或者sql语法错误")
        # else:
        #     print("没有异常时，执行的代码"（打印）)
        #  finally:
        #   self.cursor.close()
        #   self.connect.close()（无论是否异常都要执行的代码） 比如：关闭文件
        # 关闭连接（关闭游标和关闭数据库连接）释放内存
        self.cursor.close()
        self.connect.close()
        # print(sql_list)
        return sql_list



    def Through_field(self,sql_words:str, field:str):
        """遍历某个字段所有值并存到列表  field 字段名"""
        list = []
        result = self.run_mysql(sql_words)#[{一个商品的所有字段的信息}]
        for i in range(len(result)):#[{一个商品的所有字段的信息}] 列表字典的长度（个数总数）
            a = result[i][field]#字符串
            list.append(a)#把列表追加到列表中list[]
        print(list)
        return list


    # 更新操作
    def update_data(self,sql_words = ""):
        """
            更新
        :param sql_words:
        :return:
        """
        sql_update =sql_words
        try:
            self.cursor.execute(sql_update)  #像sql语句传递参数
            #提交
            self.connect.commit()
        except Exception as e:
            #错误回滚
            self.connect.rollback()
        finally:
            self.connect.close()


def run_mysql(sql_words = """"""):

    """
        运行sql语句
        :param:  sql_words: sql语句
        :return: 查询数据对应的字典列表
    """
    ### GOGO测试库
    connect = pymysql.Connect(
        host="47.99.122.18",
        port=3306,
        user="root",
        passwd="qweasd!!123",
        db="ceshi",
        charset="utf8"
    )

    # ### 测试库
    # connect = pymysql.Connect(
    #     host="rm-bp1vzoq243c7o8o4p.mysql.rds.aliyuncs.com",
    #     port=3306,
    #     user="devmmt",
    #     passwd="Bv^Pt!sVfi2fvmSq",
    #     db="mmt-mall",
    #     charset="utf8"
    # )

    ### 开发库
    # connect = pymysql.Connect(
    #     host="rm-bp1l3z2xvjyds7zv2.mysql.rds.aliyuncs.com",
    #     port=3306,
    #     user="devmmt",
    #     passwd="Bv^Pt!sVfi2fvmSq",
    #     db="dev-mmt-mall",
    #     charset="utf8"
    # )

    # 获取游标
    cursor = connect.cursor(cursor=pymysql.cursors.DictCursor)
    # 定义返回结果列表
    sql_list = []
    try:
        # 执行SQL语句
        cursor.execute(sql_words)
        connect.commit()
        # 获取所有记录列表
        results = cursor.fetchall()
        # 结果格式处理
        for i in results:
            # sql_list.append(copy.deepcopy(i))
            sql_list.append(i)
    except:
        print("Error: 无法获取数据库数据,或者sql语法错误")

    # 关闭连接
    cursor.close()
    connect.close()
    # print(sql_list)
    return sql_list #返回的列表可随便用



def Through_field(sql_words , field):
    """遍历（查看）某个字段所有值并存到列表"""
    list = []
    result = run_mysql(sql_words)
    for i in range(len(result)):
        a = result[i][field]
        list.append(a)
    # print(list)
    return list

#作用：随机生成一定范围内获取一定个数不重复的数据
def random_num(start_num:int,end_num:int,number:int): # (start_num,end_num)  产生指定起终止值中的随机整数，闭合区间 [start_num,end_num],可取到起终止值， number 20 取20个值
    import random
    random_num = random.sample(range(start_num,end_num), k = number)
    return tuple(random_num)#tuple ：元组转列表   或 列表转元祖





# db = DoDatabase()#DoDatabase类实例化
if __name__ == '__main__':
    # operadb = DoDatabase()
    # result = run_mysql("""select * from product""")
    # print(result)
    # print(result)
    # print(type(result))
    print(random_num(100,150,5))

    # Through_field("""select * from product""","product_id")