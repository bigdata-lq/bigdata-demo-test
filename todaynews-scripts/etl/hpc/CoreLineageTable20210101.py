## -*-coding:utf-8 -*-
#---------
# Name:lq
# Message: 导出血缘 0: upstream 1：downstream
# 入参 downstream ytdw dw_order_d order_id
#---------
import sys
import pymysql
import pandas as pd
import time
import numpy
params = sys.argv


coreTables = [
            'dw_order_d'
]



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

## 获取表对应的库
getDbNameSql = "select db_name from table_info where is_active = 1 and table_name = '{tableName}'"

## 血缘查询语句
downstreamTableSql = """
select downstream_db_name as db_name, downstream_table_name as table_name from data_lineage where upstream_db_name = '{dbName}' and upstream_table_name = '{tableName}' and is_active = 1 and lineage_type = 0  group by downstream_db_name, downstream_table_name
"""
upstreamTableSql = """
select upstream_db_name as db_name, upstream_table_name as table_name from data_lineage where downstream_db_name = '{dbName}' and downstream_table_name = '{tableName}' and upstream_table_name != '{tableName}'  and is_active = 1 and lineage_type != 1  group by upstream_db_name, upstream_table_name
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

coreMetaTableSql = """
    select DISTINCT table_name, db_name from table_info t 
    JOIN
    t_meta_tag m
    on t.table_id = m.meta_id
    join
    t_tag ta
    on ta.id = m.tag_id
    where ta.tag_code = 'p0_core' and t.is_active = 1 and t.meta_type = 0 and m.meta_type = 2 and t.table_name is not null;
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
    def getDbName(tableName):
        temp = MysqlUtil.read_myql("meta", getDbNameSql.format(tableName=tableName))
        if temp.empty:
            return None
        return temp.ix[[0]].values[0][0]

    @staticmethod
    def getCoreTableName():
        temp = MysqlUtil.read_myql("meta", coreMetaTableSql)
        if temp.empty:
            return None
        tables = []
        for index, row in temp.iterrows():
            tables.append(('upstream', row["db_name"], row["table_name"]))
        return tables;

    @staticmethod
    def setCoreTableLineage(result, dbName, tableName, step, sql, coreTable):
        df1 = MysqlUtil.read_myql("meta",sql.format(dbName=dbName, tableName=tableName))
        step = step + 1
        if coreTable.step < step:
            coreTable.step = step
        for index, row in df1.iterrows():
            print("第{}层血缘为：".format(step),row["db_name"], row["table_name"])
            selment = row["db_name"] + "."+ row["table_name"]
            result.add(selment)
            if dbName == row["db_name"] and tableName == row["table_name"]:
                continue
            LineageData.setCoreTableLineage(result,row["db_name"],row["table_name"],step,sql,coreTable)


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
        databaseInfo['connect_timeout'] = 200
        mysql_client = pymysql.connect(**databaseInfo)
        df = pd.read_sql(sql, mysql_client)
        df.fillna("", inplace=True)
        mysql_client.close()
        return df


class CoreTableInfo(object):

    def __init__(self, name, step):
        self.name = name
        self.step = step
        self.upstreamTableNum = 0


if __name__ == '__main__':

    ##核心任务上游链路表总和
    result = set()
    nowTime = time.strftime('%Y-%m-%d' , time.localtime())

    ##核心任务
    coreMetaTables = LineageData.getCoreTableName()
    coreMetaTables = [('upstream','ytdw','dw_order_d'),('upstream','ytdw','dw_order_tmp1')]

    ##核心任务上游链路深度
    coreTableStep = []

    ##核心链路上表引用的核心表
    tableCoreDict = {}

    for params in coreMetaTables:
        exportType = params[0]
        dbName = params[1]
        tableName = params[2]
        coreTableResult = set()
        print("start ..... export {} lineage".format(tableName))
        if len(params) == 3 and exportType == "downstream":
            print("downstream.....................")
        elif len(params) == 3 and exportType == "upstream":
            result.add(dbName + '.' + tableName)
            coreTable = CoreTableInfo(tableName,0)
            LineageData.setCoreTableLineage(coreTableResult, dbName, tableName, 0, upstreamTableSql, coreTable)
            coreTable.upstreamTableNum = len(coreTableResult)
            coreTableStep.append(coreTable)
        elif len(params) == 4 :
            print("column.....................")
        else:
            print("input params error")
            sys.exit(1)
        for name in coreTableResult :
            if name in tableCoreDict.keys():
                tableCoreDict[name] = tableCoreDict[name] + '.'+ tableName
            else:
                tableCoreDict[name] = tableName
        result = result | coreTableResult

    ## 核心链路上表
    excelName = "coreTables-" + nowTime
    path = '.'
    newResult = []
    for params in result:
        f = params.split(".")
        newResult.append((f[0],f[1],0,1))
    df = pd.DataFrame(newResult, columns = ['db_name', 'table_name','is_virtual', 'is_core'])
    df.to_csv("{path}/{excelName}.csv".format(path= path, excelName = excelName))

    ## 核心链路上游访问深度
    excelName = "coreTables-step-" + nowTime
    coreTablesStep = []
    for params in coreTableStep:
        coreTablesStep.append((params.name, params.step, params.upstreamTableNum))
    df = pd.DataFrame(coreTablesStep, columns = ['tableName', 'step', 'upstreamTableNum'])
    df.to_csv("{path}/{excelName}.csv".format(path= path, excelName = excelName))

    ## 核心链路上表引用的核心表
    excelName = "coreTables-core-" + nowTime
    coreTablesCore = []
    for key in tableCoreDict.keys():
        value = tableCoreDict[key]
        coreTablesCore.append((key, value,len(value.split("."))))
    df = pd.DataFrame(coreTablesCore, columns = ['tableName', 'coreTables','coreTablesNum'])
    df.to_csv("{path}/{excelName}.csv".format(path= path, excelName = excelName))

    print("sucess ..... export lineage")

