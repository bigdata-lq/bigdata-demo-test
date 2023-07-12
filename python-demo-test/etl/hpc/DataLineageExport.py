## -*-coding:utf-8 -*-
#---------
# Name:lq  递归导出特定需求
# Message: mysql数据迁入hdfs 隔天迁入
#---------

from etl.tools.datasource import SourceDataframe

sql1 = """
select c.db_name, c.table_name, c.column_name,c.data_type from column_info c 
join
(
select downstream_column_id,lineage_type from data_lineage where upstream_db_name = '{dbName}' and upstream_table_name = '{tableName}' and upstream_column_name = '{columnName}' and is_active = 1 
) tmp 
on c.column_id = tmp.downstream_column_id 
where c.is_active = 1 and tmp.lineage_type != 3;
"""

sql2 = """
    select db_name, table_name, column_name from column_info where is_active = 1 and db_name = 'ytdw' and table_name = 'dw_order_tmp3' and column_name != 'order_id' and sys_id = 2
"""

class PrintData(object):
    aaa = ""

    @staticmethod
    def print(dbName, tableName, columnName, step, f):
        df1 = SourceDataframe.read_myql("meta",sql1.format(dbName=dbName, tableName=tableName,
                                                          columnName=columnName))
        step = step + 1
        f = f + "   "
        for index, row in df1.iterrows():
            PrintData.aaa = PrintData.aaa + "@"
            print(step,f,row["db_name"], row["table_name"], row["column_name"])
            if step <= 4 :
                PrintData.print(row["db_name"],row["table_name"],row["column_name"],step,f)


if __name__ == '__main__':
    df = SourceDataframe.read_myql("meta", sql2)
    for index, row in df.iterrows():
        PrintData.aaa = ""
        print("'{}','{}','{}'的下游字段为：".format(row["db_name"], row["table_name"], row["column_name"]))
        PrintData.print(row["db_name"], row["table_name"], row["column_name"],0,'')




