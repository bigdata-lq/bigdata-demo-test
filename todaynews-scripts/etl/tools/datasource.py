## -*-coding:utf-8 -*-
#---------
# Name:lq
# 功能: 1.mysql数据转Dataframe 2.hive数据转dataframe
#---------
from pandas import DataFrame
from etl.tools.escript import Escript
import pymysql
from etl.settings import mysql_settings
import etl.settings
import pandas as pd



class SourceDataframe(object):

    @staticmethod
    def read_hive(hql,fields):
        """
        HQL语句返回dataframe
        """
        result = Escript().excuse_hql_result(hql,fields)
        df = DataFrame(columns=fields)
        for i, line in enumerate(result.strip().split('\n')[:-2]):
            df.loc[i] = line.split('\t')
        df.fillna("", inplace=True)
        return df

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

    @staticmethod
    def read_myql1(database):
        database = mysql_settings[database]
        print(id(mysql_settings))
        print(id(database))
        del database
        print("------")
