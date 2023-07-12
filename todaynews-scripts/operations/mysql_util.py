## -*-coding:utf-8 -*-
#---------
# Name:lq
# Message: MYSQL工具类
#---------
import pymysql
import pandas as pd


## meta jdbc参数信息
meta_settings = {
    "host": "rdsxt5l78bid42x9ddylc832.mysql.rds.aliyuncs.com:3306",
    "user": "yangtuojia001",
    "password": "yangtuojia001",
    "charset": "utf8",
    "database": "meta"
}

mysql_settings = {
    "meta": meta_settings
}

class MysqlUtil(object):

    @staticmethod
    def init_database(database):
        databaseInfo = {}
        database = mysql_settings[database]
        params = database["host"].split(":")
        databaseInfo['host'] = params[0]
        databaseInfo['port'] = int(params[1])
        databaseInfo['user'] = database['user']
        databaseInfo['password'] = database['password']
        databaseInfo['database'] = database['database']
        databaseInfo['charset'] = database['charset']
        return databaseInfo

    @staticmethod
    def read_myql(database,sql):
        """
        MYSQL语句返回dataframe
        """
        databaseInfo = MysqlUtil.init_database(database)
        mysql_client = pymysql.connect(**databaseInfo)
        df = pd.read_sql(sql, mysql_client)
        df.fillna("", inplace=True)
        mysql_client.close()
        return df

    @staticmethod
    def excuse(database, sql):
        """
        执行语句
        :param database:
        :param sql:
        :return:
        """
        databaseInfo = MysqlUtil.init_database(database)
        mysql_client = pymysql.connect(**databaseInfo)
        cursor = mysql_client.cursor()
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            mysql_client.commit()
        except Exception as e:
            print(e)
            # 如果发生错误则回滚
            mysql_client.rollback()

            # 关闭数据库连接
        mysql_client.close()
        return


    @staticmethod
    def insert_batch(database, tableName, fields, values):
        """
        批量写入数据
        """
        databaseInfo = MysqlUtil.init_database(database)
        mysql_client = pymysql.connect(**databaseInfo)
        cursor = mysql_client.cursor()
        fieldNames = ', '.join(fields)
        valuesFills = ', '.join([ '%s' for i in range(len(fields))])
        sql = "INSERT INTO {tableName} ({fieldNames}) VALUES ({valuesFills})"\
            .format(tableName = tableName, fieldNames = fieldNames, valuesFills = valuesFills)
        print(sql)
        try:
            # 执行sql语句
            cursor.executemany(sql, values)
            # 提交到数据库执行
            mysql_client.commit()
        except Exception as e:
            print(e)
            # 如果发生错误则回滚
            mysql_client.rollback()

                # 关闭数据库连接
        mysql_client.close()
        return None