#coding:utf-8
# 1、通过Hive元数据，获取到表和HDFS的对应关系
# 2、通过 pyhdfs工具类的get_content_summary方法 快速获取到占用HDFS大小
# MySQL-python==1.2.5
# PyHDFS==0.2.1
# torndb==0.3


import pyhdfs
import torndb

hive_host="idc-mysql.yangtuojia.com"
hive_port=3306
hive_database="hive"
hive_user="cmmanager"
hive_pass="PJSZty656necsapPHkFGEB7XuZUBGOXJLXX8M7M2X4S4sSvxWZGMt+l/lOiPaL+Y+lQ9UWqpx3foMkM5hpbd+Q=="

hive_metadata_client = torndb.Connection("%s:%s" %(hive_host,hive_port), hive_database, user=hive_user, password=hive_pass, time_zone='+8:00')
hdfs_client = pyhdfs.HdfsClient("http://prod-hadoop-master001:50070")



def get_db_id_list():
    sql = "select DB_ID, NAME from DBS"
    sql_result = hive_metadata_client.query(sql)

    db_id_list = []
    for elem in sql_result:
        db_id = int(elem["DB_ID"])
        db_name = str(elem["NAME"])
        db_id_list.append((db_id, db_name))
    return db_id_list


def get_sd_id_list(db_id):
    sql = "select SD_ID, TBL_NAME from TBLS where DB_ID=%s" % db_id
    sql_result = hive_metadata_client.query(sql)

    sd_id_list = []
    for elem in sql_result:
        sd_id = int(elem["SD_ID"])
        table_name = str(elem["TBL_NAME"])
        sd_id_list.append((sd_id, table_name))
    return sd_id_list


def get_table_location(sd_id):
    sql = "select LOCATION from SDS where SD_ID=%s" % sd_id
    sql_result = hive_metadata_client.query(sql)

    location = None
    for elem in sql_result:
        location = elem["LOCATION"]
    return location


def get_hdfs_size(location):
    hdfs_size = 0
    try:
        if "tesla-cluster" in location:
            location = location.split("tesla-cluster")[1]
        summary_info_dict = hdfs_client.get_content_summary(location)
        if "length" in summary_info_dict:
            hdfs_size = summary_info_dict["length"]
    except Exception as e:
        print(e)
    finally:
        return hdfs_size


def process():
    # 获取 所有数据库 db_id
    db_id_list = get_db_id_list()
    table_size_dict = {}
    for db_id, db_name in db_id_list:
        # 获取 数据库下 所有表
        sd_id_list = get_sd_id_list(db_id)
        for sd_id, table_name in sd_id_list:
            # 找到 HIVE表 对应的 HDFS目录
            location = get_table_location(sd_id)
            hdfs_size = get_hdfs_size(location)
            table_full_name = db_name + "." + table_name
            table_size_dict[table_full_name] = hdfs_size
    job_sorted_list = sorted(table_size_dict.items(), key=lambda d: d[1], reverse=True)[:100]
    print(job_sorted_list)

if __name__ == "__main__":
    process()
