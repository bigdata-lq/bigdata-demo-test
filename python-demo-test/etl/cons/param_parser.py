## -*-coding:utf-8 -*-
#-------------------------------------------------------------------------------
# Name:lq
# Message: hive业务参数
#-------------------------------------------------------------------------------
import sys
import json

list = ['/opt/cloudera/parcels/CDH-5.13.2-1.cdh5.13.2.p0.3/bin/param_parser.py', 'eval', '--connect', 'jdbc:mysql://rdsci7daxxgp4fdp1p0qv264.mysql.rds.aliyuncs.com:3306/yt_risk', '--username', 'bigdata', '--password', 'vNAPwty1sTSGo8dn', '-e', "delete from sync_risk_ads_trd_tlz_shop_summary_d where dayid < '20220324' or dayid = '20220330';"]
list = ['/opt/cloudera/parcels/CDH-5.13.2-1.cdh5.13.2.p0.3/bin/param_parser.py', 'export', '--connect', 'jdbc:mysql://rdsci7daxxgp4fdp1p0qv264.mysql.rds.aliyuncs.com:3306/yt_risk?tinyInt1isBit=false&useUnicode=true&characterEncoding=UTF-8', '--username', 'bigdata', '--password', 'vNAPwty1sTSGo8dn', '--table', 'sync_risk_ads_trd_tlz_shop_summary_d', '--fields-terminated-by', '\\001', '--input-null-string', '\\\\N', '--input-null-non-string', '\\\\N', '--export-dir', '/tmp/sync_risk_ads_trd_tlz_shop_summary_d_temp']
list = ['/opt/cloudera/parcels/CDH-5.13.2-1.cdh5.13.2.p0.3/bin/param_parser.py', 'import', '--connect', 'jdbc:mysql://pc-bp18pmc60uu8bm043.rwlb.rds.aliyuncs.com:3306/meta?tinyInt1isBit=false', '--username', 'bigdata', '--password', 'vNAPwty1sTSGo8dn', '--query', "select\n        replace(table_id,'\\t','') as table_id ,\n                replace(src_table_id,'\\t','') as src_table_id ,\n                    sys_id ,\n                replace(db_id,'\\t','') as db_id ,\n                replace(db_name,'\\t','') as db_name ,\n                replace(table_name,'\\t','') as table_name ,\n                replace(table_desc,'\\t','') as table_desc ,\n                replace(table_charset,'\\t','') as table_charset ,\n                replace(table_loc,'\\t','') as table_loc ,\n                    is_partitioned ,\n                    partition_type ,\n                replace(partition_keys,'\\t','') as partition_keys ,\n                    file_type ,\n                    life_cycle ,\n                replace(app_ids,'\\t','') as app_ids ,\n                    is_active ,\n                replace(created_by,'\\t','') as created_by ,\n                replace(updated_by,'\\t','') as updated_by ,\n                replace(create_time,'\\t','') as create_time ,\n                replace(edit_time,'\\t','') as edit_time ,\n                replace(event_time,'\\t','') as event_time ,\n                    heat ,\n                replace(remarks,'\\t','') as remarks ,\n                    host_id ,\n                replace(develop_id,'\\t','') as develop_id ,\n                    meta_type ,\n                    table_rows ,\n                    data_length ,\n                    task_status,\n                    replace(tag_ids,'\\t','') as tag_ids,\n                    sla_output_time\n                    from table_info\nwhere\n$CONDITIONS", '--target-dir', 'hdfs://hcluster/user/hadoop/target_tmp/ods_table_info_d', '--null-string', '\\\\N', '--null-non-string', '\\\\N', '--hive-table', 'ods_table_info_d', '--fields-terminated-by', '\\001', '--hive-drop-import-delims', '-m', '1']


def printSqoopParam(list):
    dict = {}

    ## 定义日志参数模型
    cmd = None
    sql_text = None
    db_connect = None
    src_db = None
    src_table = None
    to_db = None
    to_table = None
    export_dir = None
    target_dir = None

    db_name = None
    table_name = None

    if len(list) > 2 :
        cmd = "sqoop-" + list[1]

    if "--connect" in list:
        db_connect = list[list.index('--connect')+1]
        if '?' in db_connect :
            db_name = db_connect[db_connect.rfind("/") + 1:db_connect.index("?")]
        else :
            db_name = db_connect[db_connect.rfind("/") + 1:-1]


    if "--table" in list :
        table_name = list[list.index('--table')+1]

    if "-e" in list :
        sql_text = list[list.index('-e')+1]

    if "--query" in list:
        sql_text = list[list.index('--query')+1]

    if "--export-dir" in list:
        export_dir = list[list.index('--export-dir')+1]

    if "--target-dir" in list:
        target_dir = list[list.index('--target-dir')+1]


    if "import" in list:
        src_db = db_name
        src_table = table_name

    if "export" in list:
        to_db = db_name
        to_table = table_name


    dict["cmd"] = cmd
    dict["sql_text"] = sql_text
    dict["db_connect"] = db_connect
    dict["export_dir"] = export_dir
    dict["target_dir"] = target_dir
    dict["src_db"] = src_db
    dict["src_table"] = src_table
    dict["to_db"] = to_db
    dict["to_table"] = to_table
    print("YT_SQOOP_LOG: "+ json.dumps(dict))


try:
    ### 解析Sqoop入参,异常处理
    printSqoopParam(list)
except Exception as err:
    print("sqoop params parser error, exception is ", err)
else:
    print("sqoop params parser sucess....")
