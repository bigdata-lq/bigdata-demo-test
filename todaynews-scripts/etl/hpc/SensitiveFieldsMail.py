## -*-coding:utf-8 -*-
#---------
# Name:lq
# Message: 1.查出数仓表敏感字段 2.发送邮件
# 入参 downstream ytdw dw_order_d order_id
#---------


import sys
import pymysql
import pandas as pd
from impala.dbapi import connect
import binascii
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

fields = ["address",
          "phone",
          "mobile",
          "card",
          "id_number",
          "customer_name",
          "delivery_name",
          "supplier_name",
          "receiver_name",
          "receive_name ",
          "person",
          "settle_item_amount",
          "rate_amount",
          "company",
          "tax_price"]

ellipsisFields = ['ytdw.dwd_account_payable_order_item_d.settle_item_amount',
                  'ytdw.dwd_address_d.receive_phone',
                  'ytdw.dwd_address_d.receive_name',
                  'ytdw.dwd_apply_shop_d.shop_phone',
                  'ytdw.dwd_apply_shop_d.shop_address',
                  'ytdw.dwd_erp_storehouse_d.receive_phone',
                  'ytdw.dwd_erp_storehouse_d.receive_name',
                  'ytdw.dwd_gross_profit_d.settle_item_amount',
                  'ytdw.dwd_inner_orders_d.order_adress',
                  'ytdw.dwd_inner_orders_d.delivery_phone',
                  'ytdw.dwd_inner_orders_d.delivery_name',
                  'ytdw.dwd_item_batch_history_all_d.pre_tax_price',
                  'ytdw.dwd_item_batch_history_d.pre_tax_price',
                  'ytdw.dwd_order_d.order_receipt_adress',
                  'ytdw.dwd_order_d.delivery_phone',
                  'ytdw.dwd_order_d.delivery_name',
                  'ytdw.dwd_order_d.customer_phone',
                  'ytdw.dwd_order_d.customer_name',
                  'ytdw.dwd_push_info_d.receive_phone',
                  'ytdw.dwd_push_info_d.receive_name',
                  'ytdw.dwd_push_info_d.address',
                  'ytdw.dwd_seller_d.seller_company',
                  'ytdw.dwd_settle_hi_bill_detail_d.rate_amount',
                  'ytdw.dwd_settle_item_bill_d.settle_item_amount',
                  'ytdw.dwd_settle_item_bill_history_d.current_settle_item_amount',
                  'ytdw.dwd_settle_order_item_bill_d.settle_item_amount',
                  'ytdw.dwd_settle_order_item_bill_history_d.current_settle_item_amount',
                  'ytdw.dwd_settle_order_item_bill_op_d.settle_item_amount',
                  'ytdw.dwd_shop_all_d.shop_phone',
                  'ytdw.dwd_shop_all_d.shop_adress',
                  'ytdw.dwd_shop_d.shop_phone',
                  'ytdw.dwd_shop_d.shop_adress',
                  'ytdw.dwd_storehouse_d.phone',
                  'ytdw.dwd_storehouse_d.person',
                  'ytdw.dwd_supplier_apply_d.supplier_name',
                  'ytdw.dwd_supplier_order_deliver_d.delivery_phone',
                  'ytdw.dwd_supplier_order_deliver_d.delivery_name',
                  'ytdw.dwd_supplier_order_deliver_detail_d.delivery_phone',
                  'ytdw.dwd_supplier_order_deliver_detail_d.delivery_name',
                  'ytdw.dwd_supply_address_d.receiver_phone',
                  'ytdw.dwd_supply_address_d.receiver_name',
                  'ytdw.dwd_trade_shop_bu_d.detail_address',
                  'ytdw.dwd_trade_shop_bu_d.delivery_phone',
                  'ytdw.dwd_trade_shop_bu_d.delivery_name',
                  'ytdw.dwd_trade_shop_bu_d.customer_phone',
                  'ytdw.dwd_trade_shop_bu_d.customer_name',
                  'ytdw.dwd_trade_shop_bu_d.customer_id_card',
                  'ytdw.dwd_trade_shop_d.detail_address',
                  'ytdw.dwd_trade_shop_d.delivery_phone',
                  'ytdw.dwd_trade_shop_d.delivery_name',
                  'ytdw.dwd_trade_shop_d.customer_phone',
                  'ytdw.dwd_trade_shop_d.customer_name',
                  'ytdw.dwd_trade_shop_d.customer_id_card',
                  'ytdw.dwd_trade_supply_bu_d.detail_address',
                  'ytdw.dwd_trade_supply_bu_d.delivery_phone',
                  'ytdw.dwd_trade_supply_bu_d.delivery_name',
                  'ytdw.dwd_trade_supply_bu_d.customer_phone',
                  'ytdw.dwd_trade_supply_bu_d.customer_name',
                  'ytdw.dwd_trade_supply_bu_d.customer_id_card',
                  'ytdw.dwd_trade_supply_d.detail_address',
                  'ytdw.dwd_trade_supply_d.delivery_phone',
                  'ytdw.dwd_trade_supply_d.delivery_name',
                  'ytdw.dwd_trade_supply_d.customer_phone',
                  'ytdw.dwd_trade_supply_d.customer_name',
                  'ytdw.dwd_trade_supply_d.customer_id_card',
                  'ytdw.dwd_wanliniu_purchase_d.supplier_name',
                  'ytdw.dwd_wanliniu_supplier_d.supplier_name',
                  'ytdw.dw_apply_shop_info_d.shop_phone',
                  'ytdw.dw_apply_shop_info_d.shop_address',
                  'ytdw.dw_crm_shop_d.shop_phone',
                  'ytdw.dw_crm_shop_d.shop_adress',
                  'ytdw.dw_crm_shop_d.shop_adress',
                  'ytdw.dw_index_supply_item_batch_d.supply_name',
                  'ytdw.dw_order_d.settle_item_amount',
                  'ytdw.dw_order_d.pre_tax_price',
                  'ytdw.dw_order_d.detail_address',
                  'ytdw.dw_order_d.delivery_phone',
                  'ytdw.dw_order_d.delivery_name',
                  'ytdw.dw_order_d.customer_phone',
                  'ytdw.dw_order_d.customer_name',
                  'ytdw.dw_order_d.customer_id_card',
                  'ytdw.dw_order_tmp1.detail_address',
                  'ytdw.dw_order_tmp1.delivery_phone',
                  'ytdw.dw_order_tmp1.delivery_name',
                  'ytdw.dw_order_tmp1.customer_phone',
                  'ytdw.dw_order_tmp1.customer_name',
                  'ytdw.dw_order_tmp1.customer_id_card',
                  'ytdw.dw_seller_base_d.receiver_name',
                  'ytdw.dw_seller_base_d.receiver_phone ',
                  'ytdw.dw_shop_base_d.shop_phone',
                  'ytdw.dw_shop_base_d.shop_adress',
                  'ytdw.dw_shop_d.shop_phone',
                  'ytdw.dw_shop_d.shop_adress',
                  'ytdw.dw_supply_apply_d.supply_name',
                  'ytdw.dw_supply_info_detail_d.supply_company',
                  'ytdw.ods_pt_trade_shop_d.detail_address',
                  'ytdw.ods_pt_trade_shop_d.delivery_phone',
                  'ytdw.ods_pt_trade_shop_d.delivery_name',
                  'ytdw.ods_pt_trade_shop_d.customer_phone',
                  'ytdw.ods_pt_trade_shop_d.customer_name',
                  'ytdw.ods_pt_trade_shop_d.customer_id_card',
                  'ytdw.ods_pt_trade_supply_d.detail_address',
                  'ytdw.ods_pt_trade_supply_d.delivery_phone',
                  'ytdw.ods_pt_trade_supply_d.delivery_name',
                  'ytdw.ods_pt_trade_supply_d.customer_phone',
                  'ytdw.ods_pt_trade_supply_d.customer_name',
                  'ytdw.ods_pt_trade_supply_d.customer_id_card',
                  'ytdw.ods_t_account_payable_order_item_d.settle_item_amount',
                  'ytdw.ods_t_address_d.receive_phone',
                  'ytdw.ods_t_address_d.receive_name',
                  'ytdw.ods_t_apply_shop_d.shop_phone',
                  'ytdw.ods_t_apply_shop_d.shop_address',
                  'ytdw.ods_t_erp_storehouse_d.receive_phone',
                  'ytdw.ods_t_erp_storehouse_d.receive_name',
                  'ytdw.ods_t_gross_profit_d.settle_item_amount',
                  'ytdw.ods_t_inner_orders_d.order_adress',
                  'ytdw.ods_t_inner_orders_d.delivery_phone',
                  'ytdw.ods_t_inner_orders_d.delivery_name',
                  'ytdw.ods_t_item_batch_history_d.pre_tax_price',
                  'ytdw.ods_t_push_info_d.receive_phone',
                  'ytdw.ods_t_push_info_d.receive_name',
                  'ytdw.ods_t_push_info_d.address',
                  'ytdw.ods_t_seller_d.seller_company',
                  'ytdw.ods_t_settle_hi_bill_detail_d.rate_amount',
                  'ytdw.ods_t_settle_item_bill_d.settle_item_amount',
                  'ytdw.ods_t_settle_item_bill_history_d.current_settle_item_amount',
                  'ytdw.ods_t_settle_order_item_bill_d.settle_item_amount',
                  'ytdw.ods_t_settle_order_item_bill_history_d.current_settle_item_amount',
                  'ytdw.ods_t_settle_order_item_bill_op_d.settle_item_amount',
                  'ytdw.ods_t_shop_d.shop_phone',
                  'ytdw.ods_t_shop_d.shop_adress',
                  'ytdw.ods_t_storehouse_d.phone',
                  'ytdw.ods_t_storehouse_d.person',
                  'ytdw.ods_t_supplier_apply_d.supplier_name',
                  'ytdw.ods_t_supplier_order_deliver_d.delivery_phone',
                  'ytdw.ods_t_supplier_order_deliver_d.delivery_name',
                  'ytdw.ods_t_supplier_order_deliver_detail_d.delivery_phone',
                  'ytdw.ods_t_supplier_order_deliver_detail_d.delivery_name',
                  'ytdw.ods_t_supplier_order_deliver_detail_increment_d.delivery_phone',
                  'ytdw.ods_t_supplier_order_deliver_detail_increment_d.delivery_name',
                  'ytdw.ods_t_supply_address_d.receiver_phone',
                  'ytdw.ods_t_supply_address_d.receiver_name',
                  'ytdw.ods_wanliniu_purchase_d.supplier_name',
                  'ytdw.ods_wanliniu_supplier_d.supplier_name',
                  'ytdw.report_ldp_one_six_eight_hours_no_sign.column14',
                  'ytdw.report_ldp_one_six_eight_hours_no_sign.column13',
                  'ytdw.report_ldp_twenty_four_hours_no_logis.column14',
                  'ytdw.report_ldp_twenty_four_hours_no_logis.column13',
                  'ytdw.st_adminuser_coupon_pay_d.detail_address',
                  'ytdw.st_cmc_crm_act_month_current_d.shop_address',
                  'ytdw.st_cmc_crm_act_month_pre_m.shop_address',
                  'ytdw.st_cmc_crm_shop_month_current_d.shop_address',
                  'ytdw.st_cmc_crm_shop_month_pre_m.shop_address',
                  'ytdw.st_cmc_dashboard_shop_count_d.address',
                  'ytdw.st_cmc_datareport_shop_d.address',
                  'ytdw.st_crm_shopdata_d.shop_phone',
                  'ytdw.st_report_logis_dm_tmp.delivery_phone',
                  'ytdw.st_report_logis_dm_tmp.delivery_name',
                  'ytdw.st_selfhelp_order_d.detail_address',
                  'ytdw.st_selfhelp_order_d.delivery_phone',
                  'ytdw.st_selfhelp_order_d.delivery_name',
                  'ytdw.st_selfhelp_order_d.customer_phone',
                  'ytdw.st_selfhelp_order_d.customer_name',
                  'ytdw.st_selfhelp_order_d.customer_id_card',
                  'ytdw.st_selfhelp_order_tmp2.shop_phone',
                  'ytdw.st_shop_group_72h_operate_data_d.shop_phone',
                  'ytdw.st_shop_group_operate_collect_d.shop_phone',
                  'ytdw.st_shop_group_rebuy_d.shop_phone..',
                  'ytdw.ods_t_cmc_shop_d.address']

## 血缘查询语句
columnSql = """
select a.db_name, a.table_name, a.column_name, t.is_partitioned from 
(
select db_name, table_name, column_name, table_id from column_info where db_name = "ytdw" and  column_name like '%{columnName}%' and is_active = 1 and meta_type = 0 and sys_id = 2
) a join table_info t on a.table_id = t.table_id where t.is_active = 1
"""

hiveSql = """
select {columnName} from {tableName} where {wherePartition} {columnName} is not null limit 1
"""

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

    @staticmethod
    def read_hive(database,sql):
        conn = connect(host='172.16.50.4', port=10001, user='hadoop', password='JafumRvMJwajbAP2', database='ytdw', auth_mechanism="PLAIN")
        cur = conn.cursor()
        try:
            cur.execute(sql)
        except Exception as e:
            print("error sql database is {}, sql is {}, exception is {}".format(database, sql, e))
        else:
            data = cur.fetchall()
            if len(data) == 0 :
                return None
            return data[0][0]

    @staticmethod
    def is_base64_code(s):
        '''Check s is Base64.b64encode'''
        if not isinstance(s ,str) or not s:
            raise binascii.Error('params s not string or None')

        _base64_code = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                        'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                        'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a',
                        'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                        'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                        't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1',
                        '2', '3', '4','5', '6', '7', '8', '9', '+',
                        '/', '=' ]

        # Check base64 OR codeCheck % 4
        code_fail = [ i for i in s if i not in _base64_code]
        if code_fail or len(s) % 4 != 0:
            return False
        return True



if __name__ == '__main__':
    dict = {}
    result = []
    for field in fields:
        df = MysqlUtil.read_myql("meta",columnSql.format(columnName=field))
        for index, row in df.iterrows():
            dbName = row["db_name"]
            if dbName != "ytdw" :
                break
            tableName = row["table_name"]
            columnName = row["column_name"]
            isPartition = row["is_partitioned"]
            key = dbName + '.' + tableName + '.'  + columnName
            if key not in ellipsisFields:
                wherePartition = ""
                if isPartition == 1 :
                    wherePartition = """'dayid' = '20200827' and"""
                data = MysqlUtil.read_hive(dbName, hiveSql.format(tableName=tableName, columnName=columnName, wherePartition = wherePartition))
                if data and bool(1-MysqlUtil.is_base64_code(str(data))) :
                    result.append((dbName, tableName, columnName, str(data)))

    df = pd.DataFrame(result)
    df.columns = ['dbName', 'tableName','columnName',"data_example"]
    df.to_excel("数据治理敏感字段.xls")

