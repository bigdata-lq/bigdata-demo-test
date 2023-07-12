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


coreTables = [
                # 'sync_cloudatlas_new_app_homepage_report_d',
              # 'report_b_shop_repurchase_new_d',
              # 'sync_crm_st_categorygmv_d',
              # 'sync_st_kpi_indicator_achievement_d',
              # 'sync_trade_t_order_black_list',
              # 'sync_st_nrt_shop_performance_board_user_d',
              # 'sync_trade_st_order_item_rate_count_d',
              # 'st_crm_input_store_statistic_d',
              # 'sync_crm_st_contract_gmv_d',
              # 'sync_admin_st_crm_shop_brand_d',
              # 'sync_crm_st_tele_sales_shop_lost_d',
              # 'sync_crm_st_ts_achievement_brand_detail_d',
              # 'sync_crm_st_ts_achievement_sum_d',
              # 'sync_crm_st_ts_achievement_detail_d',
              # 'sync_crm_shop_group_auto_close_d',
              # 'sync_crm_st_trade_shopdata_d',
              # 'sync_crm_st_crm_shopindex_d',
              # 'sync_crm_st_crm_shopdata_d',
              # 'report_online_operator_daily',
              # 'sync_hsc_supplier_order_trend_d',
              # 'sync_afterserver_coupon_gmv_d',
              # 'sync_crm_st_trade_shopdata_d',
              # 'sync_mall_quotation_item_sale_pro_d',
              # 'sync_st_nrt_p0_subject_brand_bd_h',
              # 'sync_crm_st_p0_subject_saler_brand_ts_h',
              # 'sync_crm_st_p0_subject_saler_ts_h',
              # 'sync_st_nrt_p0_subject_shop_bd_h',
              # 'sync_st_nrt_p0_subject_ts_h',
              # 'sync_crm_st_salary_summary_data_d',
              # 'sync_crm_st_p0_subject_plan_sum_d',
              # 'sync_crm_st_p0_subject_rule_detail_d',
              # 'sync_st_nrt_shop_performance_board_dept_d',
              # 'sync_risk_financial_factor_d',
              # 'sync_risk_supply_indicator_d',
              # 'sync_supplier_st_supplier_score_source_d',
              # 'sync_recon_nrt_predict_cash_original',
              # 'sync_hmc_flashbuy_dapan_d',
              # 'sync_risk_st_adminuser_fund_account_base_d',
              # 'dw_coupon_use_d',
              # 'dw_supply_info_detail_d',
              # 'sync_hsc_supplier_order_sum_d',
              # 'sync_hsc_supplier_order_item_sum_d',
              # 'sync_hsc_supplier_order_brand_sum_d',
              # 'sync_hsc_supplier_order_area_sum_d',
              # 'sync_supplier_st_supplier_score_statistics_source_d',
              # 'report_seller_rule_auditor_data',
              # 'sync_cloudatlas_st_app_element_analysis_d',
              # 'sync_cloudatlas_st_app_element_h',
              # 'sync_malltoc_shop_front_category_d',
              # 'sync_hsc_supplier_order_item_sum_h',
              # 'sync_hsc_supplier_order_brand_sum_h',
              # 'sync_hsc_supplier_order_area_sum_h',
              # 'sync_hsc_supplier_order_sum_yesterday_d',
              # 'sync_hsc_supplier_order_item_sum_yesterday_d',
              # 'sync_hsc_supplier_order_brand_sum_yesterday_d',
              # 'sync_hsc_supplier_order_area_sum_yesterday_d',
              # 'sync_crm_st_nrt_hiking_bd_server_data',
              # 'sync_crm_st_nrt_hiking_bd_area_data',
              # 'nrt_order_wide_new',
              # 'sync_cloudatlas_st_cloudatlas_operation_d',
              # 'dw_brand_info_d',
              # 'dw_item_d',
              # 'report_seller_item_category_d',
              # 'dw_item_index_info_d',
              # 'dw_item_index_info_new_d',
              # 'sync_cloudatlas_st_app_itemdetail_d',
              # 'sync_search_st_item_popularity_d'
              'sync_admin_st_supplier_data_d',
              'sync_admin_st_supplier_data_d',
              'sync_admin_st_supplier_user_data_d',
              'sync_admin_st_supplier_gmv_data_d',
              'sync_admin_st_supplier_gmv_d',
              'sync_admin_st_supplier_gmv_category_d',
              'sync_admin_st_supplier_gmv_top_item_d',
              'sync_admin_st_supplier_gmv_top_brand_d',
              'sync_admin_st_supplier_service_d',
              'sync_admin_st_supplier_service_top_brand_d',
              'sync_admin_st_supplier_service_top_item_d',
              'sync_admin_st_supplier_gmv_area_d',
              'sync_mall_st_recplat_model_result_itemdetail_d',
              'report_buried_code_pv_monitor_d',
              'sync_admin_st_punish_order_item',
              'sync_admin_st_punish_order_logistics',
              'sync_crm_input_store_statistic_d',
              'report_custom_confirm_collect_d',
              'report_search_daily_total_d',
              'report_search_daily_match_d',
              'sync_st_shop_group_operate_collect_v2_d',
              'report_search_daily_item_d',
              'dw_order_d',
              'dw_flw_visit_trace_di',
              'dw_flw_exposure_trace_di',
              'dwd_user_d',
              'report_new_sign_success_shop_d',
              'sync_hsp_st_service_providers_brand_d',
              'sync_hsp_st_service_providers_summay_d',
              'st_sp_list_report_d',
              'sync_hsp_st_shop_data_brand_d',
              'sync_hsp_st_shop_data_sp_d',
              'dw_gross_profit_all_d',
              'sync_cloudatlas_app_activity_transform_report',
              'sync_cloudatlas_st_app_activity_item_detail_report_d',
              'sync_cloudatlas_app_activity_detail_report',
              'sync_crm_st_salary_summary_data_d',
              'sync_crm_recommend_visit_d',
              'sync_crm_st_brand_search_d',
              'sync_crm_st_btype_brand_opt_d',
              'sync_st_crm_month_btype_brand_d',
              'sync_crm_st_hiking_bd_server_data_d',
              'sync_crm_st_hiking_bd_area_data_d',
              'sync_st_sales_wxchat_summary_d',
              'sync_crm_st_sales_quality_summary_d',
              'eport_online_operator_daily',
              'dw_material_relay_info_d',
              'sync_smc_shop_transform_ratio_d',
              'sync_smc_straightcut_item_data_d',
              'sync_smc_straightcut_unitprice_d',
              'st_selfhelp_order_new_d',
              'dw_order_trade_supply_simple_d',
              'report_hi_card_month_data',
              'report_finance_coupon_mail',
              'dw_gross_profit_all_effective_d',
              'report_super_category_date',
              'dw_operate_data_center_v2_d',
              'dws_trd_item_td',
              'dws_flw_item_1d',
              'dws_flw_key_word_1d',
              'dw_item_complex_index_d',
              'dw_brand_complex_index_d',
              'st_report_apps_daily_d',
              'dw_operate_data_center_visit_filter_d',
              'dw_operate_data_center_search_visit_d',
              'dw_shop_visit_filter_d',
              'dw_order_pre_trace_d',
              'dw_activity_board_base_d',
              'dw_tele_sales_shop_d',
              'dw_tele_sales_order_v2_d',
              'refund_order_report_d',
              'dw_shop_base_d',
              'st_shop_transfer_base_data_d',
              'sync_admin_dw_index_refund_ratio_d',
              'sync_bi_dw_order_d_for_wxd',
              'sync_st_suyuanma_guanlian',
              'sync_st_suyuanma_guanlian_logi',
              'sync_punish_order',
              'sync_shop_list',
              'report_slient_successful_shop_d',
              'sync_supply_fund_serial_record_d',
              'sync_mall_st_recplat_model_result_d',
              'sync_mall_st_recplat_model_result_sy01_d'
]



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

## 获取表对应的库
getDbNameSql = "select db_name from table_info where is_active = 1 and table_name = '{tableName}'"

## 血缘查询语句
downstreamTableSql = """
select downstream_db_name as db_name, downstream_table_name as table_name from data_lineage where upstream_db_name = '{dbName}' and upstream_table_name = '{tableName}' and is_active = 1 and lineage_type = 0  group by downstream_db_name, downstream_table_name
"""
upstreamTableSql = """
select upstream_db_name as db_name, upstream_table_name as table_name from data_lineage where downstream_db_name = '{dbName}' and downstream_table_name = '{tableName}' and is_active = 1 and lineage_type != 1  group by upstream_db_name, upstream_table_name
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
    def changeLineage(result):
        
        return result


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
        return df


if __name__ == '__main__':

    result = []
    coreMetaTables = []

    for tableName in coreTables:
        dbName = LineageData.getDbName(tableName)
        if dbName:
            coreMetaTables.append(('upstream',dbName,tableName))
        else:
            print(" {} 对应的库不存在".format(tableName))

    print(coreMetaTables)
    for params in coreMetaTables:
        exportType = params[0]
        dbName = params[1]
        tableName = params[2]
        colName = ""
        columnTabs = ['层级', '库名', '表名']
        print("start ..... export {} lineage".format(tableName))
        if len(params) == 3 and exportType == "downstream":
            result.append((0, dbName, tableName))
            LineageData.setTableLineage(result, dbName, tableName, 0, downstreamTableSql)
        elif len(params) == 3 and exportType == "upstream":
            result.append((0, dbName, tableName))
            LineageData.setTableLineage(result, dbName, tableName, 0, upstreamTableSql)
        elif len(params) == 4 :
            colName = params[3]
            dataType = LineageData.getColumnDataType(dbName, tableName, colName)
            result.append((0, dbName, tableName,colName,dataType))
            if exportType == "downstream":
                LineageData.setColumnLineage(result, dbName, tableName, colName, 0, downstreamColumnSql)
            elif exportType == "upstream":
                LineageData.setColumnLineage(result, dbName, tableName, colName, 0, upstreamColumnSql)
            else:
                print("input params error")
                sys.exit(1)
        else:
            print("input params error")
            sys.exit(1)

        if len(colName) > 0 :
            columnTabs.append("字段名")
            columnTabs.append("字段类型")
    excelName = "coreTables"
    df = pd.DataFrame(result)
    df.columns = columnTabs
    df.to_excel("{excelName}.xlsx".format(excelName = excelName))
    print("sucess ..... export lineage")

