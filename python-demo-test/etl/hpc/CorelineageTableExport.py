## -*-coding:utf-8 -*-
#---------
# Name:lq
# Message: 导出血缘 0: upstream 1：downstream
# 入参 downstream ytdw dw_order_d order_id
#---------
import sys
import pymysql
import pandas as pd
params = sys.argv


## meta jdbc参数信息
meta_settings = {
    "host": "pc-bp18pmc60uu8bm043.rwlb.rds.aliyuncs.com:3306",
    "user": "streaming_pdb",
    "password": "xOMZ0AbeeIlKDqyi",
    "charset": "utf8",
    "database": "meta"
}

mysql_settings = {
    "meta": meta_settings
}

## 血缘查询语句
downstreamTableSql = """
select downstream_db_name as db_name, downstream_table_name as table_name from data_lineage where upstream_db_name = '{dbName}' and upstream_table_name = '{tableName}' and is_active = 1 and lineage_type = 0  group by downstream_db_name, downstream_table_name
"""
upstreamTableSql = """
select upstream_db_name as db_name, upstream_table_name as table_name from data_lineage where downstream_db_name = '{dbName}' and downstream_table_name = '{tableName}' and is_active = 1 and lineage_type = 0 group by upstream_db_name, upstream_table_name
"""

downstreamColumnSql = """
select c.db_name, c.table_name, c.column_name, c.data_type from column_info c 
join
( select distinct downstream_column_id from data_lineage where upstream_db_name = '{dbName}' and upstream_table_name = '{tableName}' and upstream_column_name = '{columnName}' and is_active = 1 and lineage_type = 0 ) tmp 
on c.column_id = tmp.downstream_column_id where c.is_active = 1 and c.sys_id = 2 and c.meta_type = 0
"""

upstreamColumnSql = """
select c.db_name, c.table_name, c.column_name, c.data_type from column_info c 
join
( select distinct upstream_column_id from data_lineage where downstream_db_name = '{dbName}' and downstream_table_name = '{tableName}' and downstream_column_name = '{columnName}' and is_active = 1 and lineage_type = 0 ) tmp 
on c.column_id = tmp.upstream_column_id where c.is_active = 1 and c.sys_id = 2 and c.meta_type = 0
"""

columnDetailSql = """
    select data_type from column_info where db_name = '{dbName}' and table_name = '{tableName}' and column_name = '{columnName}' and is_active = 1 and meta_type = 0 and sys_id = 2
"""

class LineageData(object):

    @staticmethod
    def setColumnLineage(result, dbName, tableName, columnName, step, sql):
        df1 = MysqlUtil.read_myql("meta",sql.format(dbName=dbName, tableName=tableName,
                                                           columnName=columnName))
        step = step + 1
        for index, row in df1.iterrows():
            print("第{}层血缘为：".format(step), row["db_name"], row["table_name"], row["column_name"], row["data_type"])
            result.append((step, row["db_name"], row["table_name"], row["column_name"], row["data_type"]))
            if dbName == row["db_name"] and tableName == row["table_name"] and columnName == row["column_name"] :
                continue
            LineageData.setColumnLineage(result,row["db_name"],row["table_name"],row["column_name"],step,sql)


    @staticmethod
    def setTableLineage(result, dbName, tableName, step, sql):
        df1 = MysqlUtil.read_myql("meta",sql.format(dbName=dbName, tableName=tableName))
        step = step + 1
        for index, row in df1.iterrows():
            print("第{}层血缘为：".format(step),row["db_name"], row["table_name"])
            result.append((step, row["db_name"], row["table_name"]))
            if dbName == row["db_name"] and tableName == row["table_name"]:
                continue
            LineageData.setTableLineage(result,row["db_name"],row["table_name"],step,sql)

    @staticmethod
    def getColumnDataType(dbName, tableName, columnName):
        temp = MysqlUtil.read_myql("meta", columnDetailSql.format(dbName= dbName, tableName=tableName,
                                                             columnName=columnName))
        return temp.ix[[0]].values[0][0]

    @staticmethod
    def changeLineage(result):
        
        return result


class MysqlUtil(object):

    @staticmethod
    def read_myql(database,sql):
        """
        MYSQL语句返回dataframe
        """
        databaseInfo = {}
        database = mysql_settings[database]
        params = database["host"].split(":")
        databaseInfo['host'] = params[0]
        databaseInfo['port'] = int(params[1])
        databaseInfo['user'] = database['user']
        databaseInfo['password'] = database['password']
        databaseInfo['database'] = database['database']
        databaseInfo['charset'] = database['charset']
        mysql_client = pymysql.connect(**databaseInfo)
        df = pd.read_sql(sql, mysql_client)
        df.fillna("", inplace=True)
        mysql_client.close()
        return df


if __name__ == '__main__':
    print('input params is:', str(params))
    result = []
    params.pop(0)
    exportType = params[0]
    dbName = params[1]
    tableName = params[2]
    colName = ""
    columnTabs = ['层级', '库名', '表名']
    print("start ..... export lineage")
    if len(params) == 3 and exportType == "downstream":
        result.append((0, dbName, tableName))
        LineageData.setTableLineage(result, dbName, tableName, 0, downstreamTableSql)
    elif len(params) == 3 and exportType == "upstream":
        result.append((0, dbName, tableName))
        LineageData.setTableLineage(result, dbName, tableName, 0, upstreamTableSql)
    elif len(params) == 4 :
        colName = params[3]
        dataType = LineageData.getColumnDataType(dbName, tableName, colName)
        result.append((0, dbName, tableName,colName,dataType))
        if exportType == "downstream":
            LineageData.setColumnLineage(result, dbName, tableName, colName, 0, downstreamColumnSql)
        elif exportType == "upstream":
            LineageData.setColumnLineage(result, dbName, tableName, colName, 0, upstreamColumnSql)
        else:
            print("input params error")
            sys.exit(1)
    else:
        print("input params error")
        sys.exit(1)

    if len(colName) > 0 :
        columnTabs.append("字段名")
        columnTabs.append("字段类型")
    excelName = '_'.join(params)
    df = pd.DataFrame(result)
    df.columns = columnTabs
    df.to_excel("{excelName}.xls".format(excelName = excelName))
    print("sucess ..... export lineage")

