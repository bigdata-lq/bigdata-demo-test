## -*-coding:utf-8 -*-
#---------
# Name:lq
# Message: 1.hive数据全量迁移mysql 2.mysql数据全量迁移hive 3.mysql数据增量迁移hive 4.执行hive脚本 5.执行shell脚本
#---------
from etl.tools.mysshclient import MySSHClient
from etl.cons.data_param import Param
from etl.settings import mysql_settings,hive_settings,spark_settings


class Escript(object):

    def __init__(self,flag = False, type = 'm_eps'):
        """
        :flag False 跳转hive True 跳转spark
        :type 不同的mysql库
        """
        dicts = {}
        Param(dicts)
        self.ssh = MySSHClient(flag = flag)
        self.dicts = dicts
        self.mysql_settings = mysql_settings[type]


    def e_sqoop_hive2myql(self, hpath, mname, fields, parallelism=1):
        """
        功能：迁移hive --> mysql 全量迁移(先删除，再迁移)
        分区迁移和更新迁移未做
        :param hpath: hive 数据存储目录
        :param mname: mysql表名称
        :return:
        """
        database=self.mysql_settings['database']
        print('【大数据组】清空 {} 表'.format(mname))
        delSql = """sqoop eval \
                      --connect jdbc:mysql://{host}/{database}?characterEncoding=utf8 \
                      --username {user} \
                      --password {password} \
                      --query 'delete from {mname}'
                      """.format(host=self.mysql_settings["host"], database=database, user=self.mysql_settings["user"]
                                 , password=self.mysql_settings["password"], mname = mname)
        print('【大数据组】清空表sqoop语句为： {} '.format(delSql.replace('\n', '')))
        self.excuse_hql(delSql)
        print('【大数据组】开始迁移： {} 路径数据到 {} 表中'.format(hpath, mname))
        sqpSql =  """sqoop export \
                        --connect jdbc:mysql://{host}/{database}?characterEncoding=utf8 \
                        --username {user} \
                        --password {password} \
                        --table  {mname} \
                        --export-dir {hpath} \
                        --columns {fields} \
                        --input-fields-terminated-by '\001' \
                        --input-null-string '' \
                        --input-null-non-string '' \
                        --m {parallelism}
                        """.format(host=self.mysql_settings["host"], database=database, user=self.mysql_settings["user"],fields=fields
                                   , password=self.mysql_settings["password"], mname = mname, hpath = hpath, parallelism=parallelism)
        print('【大数据组】迁移hive表sqoop语句为： {} '.format(sqpSql.replace('\n', '')))
        self.excuse_hql(sqpSql)


    def e_sqoop_increment_mysql2hive(self, htablename, hpath, mname, dayNum=0, parallelism=1):
        """
         功能：增量迁移mysql --> hive 1.按天新增 2.去除分隔符
         :param hpath: hive 数据存储目录
         :param mname: mysql表名称
         :return:
        """
        database=self.mysql_settings['database']
        dicts = Param.get_last_day(dayNum)
        start_day = dicts['ARG_TODAY_START']
        end_day = dicts['ARG_TODAY_END']
        query_where='gmt_create >= \\"{start_day}\\" and gmt_create < \\"{end_day}\\"'.format(start_day=start_day, end_day=end_day)
        print('【大数据组】迁移表{}, 迁移条件为： {} '.format(mname,query_where.replace('\n', '')))
        hpath = hpath + start_day
        shellsql =  """sqoop import \
                    --connect jdbc:mysql://{host}/{database}?tinyInt1isBit=false \
                    --username {user} \
                    --password {password} \
                    --fields-terminated-by '\001' \
                    --target-dir {hpath} \
                    --table {mname} --where '{query_where}' \
                    --delete-target-dir  \
                    --hive-drop-import-delims \
                    --null-string '' \
                    --null-non-string '' \
                    --m {parallelism}
                    """.format(host=self.mysql_settings["host"], database=database, user=self.mysql_settings["user"]
                               , password=self.mysql_settings["password"], mname = mname, hpath = hpath, query_where=query_where, parallelism=parallelism)
        print('【大数据组】迁移hive表sqoop语句为： {} '.format(shellsql.replace('\n', '')))
        self.excuse_hql(shellsql)
        print('【大数据组】开始映射数据： {} '.format(htablename.replace('\n', '')))
        self.e_h_partition(htablename, hpath, start_day)

    def e_sqoop_whole_mysql2hive(self, hpath,mname, field = 'gmt_create', parallelism=1):

        """
         功能：全表迁移 截止时间今天凌晨
         :param hpath: hive 数据存储目录
         :param mname: mysql表名称
         :return:
        """
        database=self.mysql_settings['database']
        end_day = self.dicts["ARG_TODAY_ISO"]
        query_where='{field} < \\"{end_day}\\"'.format(field = field,end_day=end_day)
        print('【大数据组】迁移表{}, 迁移条件为： {} '.format(mname,query_where.replace('\n', '')))
        shellsql =  """sqoop import \
                    --connect jdbc:mysql://{host}/{database}?tinyInt1isBit=false \
                    --username {user} \
                    --password {password} \
                    --fields-terminated-by '\001' \
                    --target-dir {hpath} \
                    --table {mname} --where '{query_where}' \
                    --delete-target-dir  \
                    --hive-drop-import-delims \
                    --null-string '' \
                    --null-non-string '' \
                    --m {parallelism}
                    """.format(host=self.mysql_settings["host"], database=database, user=self.mysql_settings["user"],parallelism=parallelism
                               , password=self.mysql_settings["password"], mname = mname, hpath = hpath, query_where=query_where)
        print('【大数据组】迁移hive表sqoop语句为： {} '.format(shellsql.replace('\n', '')))
        self.excuse_hql(shellsql)
        self.ssh.close()

    def e_h_partition(self, htablename, hpath, partition):
        """
         按照分区映射数据
         :param htablename hive库.表名
         :hpath hdfs数据存储地址
         :partition 分区时间 %Y-%m-%d
         :return:
        """
        hql =   """
                ALTER TABLE {htablename} ADD PARTITION (dt='{partition}') LOCATION '{hpath}'
                """.format(htablename=htablename, partition=partition, hpath=hpath)
        print('【大数据组】映射语句为： {} '.format(hql.replace('\n', '')))
        self.excuse_hql(hql, flag=True)

    def excuse_hql(self, hql, flag = False):
        """
         功能：执行hive脚本
         :return:
        """
        # os.system('hive -e "%s"' % hql)
        ssh=self.ssh

        if flag:
            hql = 'hive -e \\"%s\\"' % hql
        hql='su - hdfs -s /bin/bash -c "{}"'.format(hql)
        ssh.run(hql)


    def excuse_hql_result(self, hql, fields = []):
        """
         功能：执行hive脚本
         :return: 返回执行结果
        """
        ssh=self.ssh
        hql = 'hive -e \\"%s\\"' % hql
        # stdin, stdout, stderr = ssh.exec_command(hql)#执行命令并获取命令结果
        # res,err = stdout.read(),stderr.read()
        hql='su - hdfs -s /bin/bash -c "{}"'.format(hql)
        result = ssh.run(hql)
        ssh.close()
        return result




