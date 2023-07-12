## -*-coding:utf-8 -*-
#---------
# Name:lq  递归导出特定需求
# Message: mysql数据迁入hdfs 隔天迁入
#---------

from etl.tools.datasource import SourceDataframe

### 查询表下游血缘
sql1 = """
select downstream_db_name as db_name, downstream_table_name as table_name from data_lineage 
where upstream_db_name = '{dbName}' and upstream_table_name = '{tableName1}'  and is_active = 1 and lineage_type = 0 
and downstream_table_name != '{tableName2}'
group by downstream_db_name, downstream_table_name
"""

### 查询表上游血缘
sql2 = """
select upstream_db_name as db_name, upstream_table_name as table_name from data_lineage 
where downstream_db_name = '{dbName}' and downstream_table_name = '{tableName1}'  and is_active = 1 and lineage_type = 0 
and upstream_table_name != '{tableName2}'
group by downstream_db_name, downstream_table_name
"""

class PrintData(object):
    aaa = ""
    @staticmethod
    def print(dbName, tableName, step, f, list):
        df1 = SourceDataframe.read_myql("meta",sql1.format(dbName=dbName, tableName1=tableName, tableName2=tableName))
        step = step + 1
        f = f + "   "
        for index, row in df1.iterrows():
            PrintData.aaa = PrintData.aaa + "@"
            print(step,f,row["db_name"], row["table_name"])
            list.append(row["db_name"] + "." + row["table_name"])
            PrintData.print(row["db_name"],row["table_name"], step, f, list)

    @staticmethod
    def print1(dbName, tableName, step, f, list, dict1, dict2):
        df1 = SourceDataframe.read_myql("meta",sql1.format(dbName=dbName, tableName1=tableName, tableName2=tableName))
        step = step + 1
        f = f + "   "
        for index, row in df1.iterrows():
            PrintData.aaa = PrintData.aaa + "@"
            print(step,f,row["db_name"], row["table_name"])
            list.append(row["db_name"] + "." + row["table_name"])
            PrintData.print(row["db_name"],row["table_name"], step, f, list)

if __name__ == '__main__':
    list = [] ## 存放所有下游表
    dict1 = {} ## 可以确定层级
    dict2 = {} ## 不可以确定层级
    PrintData.print('ytdw', 'dw_item_d', 0,'', list)

    PrintData.print1('ytdw', 'dw_item_d', 0,'', list, dict1, dict2)




