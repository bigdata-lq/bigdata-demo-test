
import json
str = """
meta_name, meta_type, meta_id,
meta_sys_url, num_field_1, num_field_2,
num_field_3, num_field_4, num_field_5,
num_field_6, num_field_7, num_field_8,
str_field_1, str_field_2, str_field_3,
str_field_4, str_field_5, str_field_6,
str_field_7, arr_field_6, arr_field_5,
arr_field_4, arr_field_1, arr_field_2,
arr_field_3, data_create_time, date_edit_time,
expose_num, click_num, create_time,
edit_time
"""

list = str.split(",")

for i in list:
    print(i.strip() + " = VALUES(" +i.strip() +"),")



str = """
{
  "id": 1,
  "type": 1,
  "typeName": "demoData",
  "cnName": "demoData",
  "enName": "demoData",
  "bizOwnerId": "demoData",
  "bizOwnerName": "demoData",
  "devOwnerId": "demoData",
  "devOwnerName": "demoData",
  "bizDefinition": "demoData",
  "dbName": "demoData",
  "tableName": "demoData",
  "pkName": "demoData",
  "pkCnName": "demoData",
  "subjectDomainNames": "demoData",
  "bizProcessNames": "demoData",
  "calcLogic": "demoData",
  "createTimeStr": "demoData",
  "editTimeStr": "demoData"
}
"""

d = json.loads(str)

# insert into t_meta_search_schame (meta_type, column_code) value(8,'id')
for key in d.keys():
    print("insert into t_meta_search_schame (meta_type, column_code) value(9,'" + key + "');")
