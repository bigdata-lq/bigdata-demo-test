## -*-coding:utf-8 -*-
#---------
# Name:lq
# Message: mysql表映射成hive表
#---------

from etl.tools.datasource import SourceDataframe
import re
mapping = {
    "int":"int",
    "varchar":"string",
    "char":"string",
    "blob":"tinyint",
    "text":"string",
    "integer":"bigint",
    "boolean":"boolean",
    "tinyint":"tinyint",
    "smallint":"smalint",
    "mediumint":"int",
    "bit":"boolean",
    "bigint":"bigint",
    "float":"float",
    "double":"double",
    "decimal":"decimal",
    "boolean":"boolean",
    "id":"bigint",
    "date":"date",
    "datetime":"timestamp",
    "time":"string",
    "timestamp":"timestamp",
    "year":"date"
}


class HiveUtil(object):

    @staticmethod
    def changeMysql2Hive(database, tablename, path):
        schemeDf = SourceDataframe.read_myql(database=database,sql="show full columns from {}".format(tablename))
        dt = "aishangtoutiao.m_"+ tablename
        hiveschame = "create external table if not exists {} (\n".format(dt)
        hiveschame = '\n'.join(['################# {} #################'.format(dt),hiveschame])
        for index,row in schemeDf.iterrows():
            type = re.sub('\\(.*?\\)','',row['Type'])
            type = type.replace('unsigned', '').strip()
            type = mapping[type]
            # print(row['Field'],type,row['Comment'])
            hiveschame += ' '.join([row['Field'],type,"comment '{}'".format(row['Comment']),",\n"])
        hiveschame = hiveschame[:-2]
        hiveschame = '\n'.join([hiveschame.strip(),')', 'row format delimited', "fields terminated by '\\001'", 'stored as textfile',
                                "location '{}';".format(path)
                                ])+ '\n'
        print(hiveschame)
        HiveUtil.save("./hivetable.sql",hiveschame)
        return hiveschame

    @staticmethod
    def save(filename, contents):
        fh = open(filename, 'a+', encoding='utf-8')
        fh.write(contents)
        fh.close()

