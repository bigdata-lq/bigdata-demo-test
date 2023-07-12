

print(3232)


aaa = """
{"export_dir": null, "to_db": null, "src_table": null, "target_dir": "hdfs://hcluster/user/hadoop/target_tmp/ods_act_hi_varinst_d", "cmd": "sqoop-import", "sql_text": "select\n replace(id_,'\\t','') as id_ ,\n replace(proc_inst_id_,'\\t','') as proc_inst_id_ ,\n replace(execution_id_,'\\t','') as execution_id_ ,\n replace(task_id_,'\\t','') as task_id_ ,\n replace(name_,'\\t','') as name_ ,\n replace(var_type_,'\\t','') as var_type_ ,\n rev_ ,\n replace(bytearray_id_,'\\t','') as bytearray_id_ ,\n double_ ,\n long_ ,\n replace(text_,'\\t','') as text_ ,\n replace(text2_,'\\t','') as text2_ ,\n replace(create_time_,'\\t','') as create_time_ ,\n replace(last_updated_time_,'\\t','') as last_updated_time_ from act_hi_varinst\nwhere\n$CONDITIONS", "src_db": "yt_hioa", "to_table": null, "db_connect": "jdbc:mysql://pc-bp18pmc60uu8bm043.rwlb.rds.aliyuncs.com:3306/yt_hioa?tinyInt1isBit=false"}
"""


aaa = aaa.replace("\n", "")
print(aaa)


sql_text = 1212
if sql_text:
    print(1122)