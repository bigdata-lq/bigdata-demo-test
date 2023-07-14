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
    "host": "rm-bp10q4q9cwc1f267p717.mysql.rds.aliyuncs.com:3306",
    "user": "group_data",
    "password": "GJvSbAn84Y9mIFRx",
    "charset": "utf8",
    "database": "meta"
}

mysql_settings = {
    "meta": meta_settings
}

## 血缘查询语句

upstreamTableSql = """
select upstream_db_name as db_name, upstream_table_name as table_name from data_lineage where downstream_db_name = '{dbName}' and downstream_table_name = '{tableName}' and is_active = 1 and lineage_type = 0 group by upstream_db_name, upstream_table_name
"""


mysqlTableSql = """
    select db_name dbName from table_info where table_name = '{tableName}' and is_active = 1 and meta_type = 1 and LENGTH(db_name) < 15
"""

class LineageData(object):

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
    def getMysqlDbName(tableName):
        temp = MysqlUtil.read_myql("meta", mysqlTableSql.format(tableName=tableName))
        if temp.empty:
            temp = MysqlUtil.read_myql("meta", mysqlTableSql.format(tableName=tableName + '_0'))
            if temp.empty:
                return None
            else:
                print("分表表名为"+ tableName + '_0')
        return temp['dbName'][0]


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
        return



if __name__ == '__main__':
    coreTables = [('kylin','dws_flw_item_1d'),
                  ('kylin','dws_trd_item_td'),
                  ('ytdw','dw_brand_info_d'),
                  ('ytdw','dw_coupon_use_d'),
                  ('ytdw','dw_gross_profit_all_d'),
                  ('ytdw','dw_gross_profit_all_effective_d'),
                  ('ytdw','dw_item_d'),
                  ('ytdw','dw_item_index_info_d'),
                  ('ytdw','dw_item_index_info_new_d'),
                  ('ytdw','dw_operate_data_center_v2_d'),
                  ('ytdw','dw_order_trade_supply_simple_d'),
                  ('ytdw','dw_shop_base_d'),
                  ('ytdw','dw_supply_info_detail_d'),
                  ('ytdw','dw_tele_sales_order_v2_d'),
                  ('ytdw','dw_tele_sales_shop_d'),
                  ('ytdw','nrt_order_wide_new'),
                  ('ytdw','refund_order_report_d'),
                  ('ytdw','report_finance_coupon_mail'),
                  ('ytdw','report_hi_card_month_data'),
                  ('ytdw','report_new_sign_success_shop_d'),
                  ('ytdw','report_online_operator_daily'),
                  ('ytdw','report_seller_rule_auditor_data'),
                  ('ytdw','report_slient_successful_shop_d'),
                  ('ytdw','report_super_category_date'),
                  ('ytdw','st_selfhelp_order_new_d'),
                  ('ytdw','st_new_app_activity_detail_report_d'),
                  ('ytdw','st_new_app_activity_transform_report_d'),
                  ('ytdw','st_new_app_activity_item_detail_report_d'),
                  ('ytdw','st_crm_input_store_statistic_d'),
                  ('ytdw','st_crm_shop_group_auto_close_d'),
                  ('ytdw','st_categorygmv_d'),
                  ('ytdw','st_crm_shopdata_d'),
                  ('ytdw','st_crm_shopindex_d'),
                  ('ytdw','dw_salary_summary_data_d'),
                  ('ytdw','dw_shop_ab_level_d'),
                  ('ytdw','st_shop_tradedata_d'),
                  ('ytdw','st_service_providers_d'),
                  ('ytdw','st_shop_front_category_d'),
                  ('ytdw','st_quotation_item_sale_info_d'),
                  ('ytdw','st_crm_sales_kpi_indicator_achievement_d'),
                  ('ytdw','st_shop_group_operate_collect_v2_d'),
                  ('ytdw','st_ord_black_list'),
                  ('ytdw','st_p0_subject_plan_sum_d'),
                  ('ytdw','st_p0_subject_rule_detail_d')]

    print("start ..... analyse lineage")
    allDbHiveTable = []
    for coreTable in coreTables:
        result = []
        hiveDbName = coreTable[0]
        hiveTableName = coreTable[1]
        result.append((0, hiveDbName, hiveTableName))
        LineageData.setTableLineage(result, hiveDbName, hiveTableName, 0, upstreamTableSql)

        dbNameAndHiveTableName = []
        dbNames = []
        tableNames = []
        for i in result:
            tableName = (str)(i[2])
            if tableName.startswith("ods_") and tableName not in tableNames:
                mysqlTableName = tableName[4:len(tableName)-2]
                mysqlDbName = LineageData.getMysqlDbName(mysqlTableName)
                tableNames.append(tableName)
                if mysqlDbName and mysqlDbName not in dbNames:
                    dbNames.append(mysqlDbName)
                    dbNameAndHiveTableName.append((mysqlDbName, hiveDbName + "." + hiveTableName))
        if not dbNameAndHiveTableName:
            print(coreTable,'表初始库出错.....')
        print(dbNameAndHiveTableName)
        allDbHiveTable.extend(dbNameAndHiveTableName)


    dbHiveTableDict = {}
    for i in allDbHiveTable:
        dbName = i[0]
        coreHiveTableName = i[1]
        if dbName not in dbHiveTableDict:
            dbHiveTableDict[dbName] = coreHiveTableName
        else:
            dbHiveTableDict[dbName] = dbHiveTableDict[dbName] + "|" + coreHiveTableName

    for i in dbHiveTableDict:   #遍历字典中的键
        print('mysql库：', i, 'hive核心表',dbHiveTableDict[i])
