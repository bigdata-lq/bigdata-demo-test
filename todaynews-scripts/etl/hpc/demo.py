## -*-coding:utf-8 -*-
#---------
# Name:lq  递归导出特定需求
# Message: mysql数据迁入hdfs 隔天迁入
#---------

from etl.tools.datasource import SourceDataframe
import pandas as pd

sql1 = """
select c.db_name, c.table_name, c.column_name, c.data_type from column_info c 
join
(
select downstream_column_id from data_lineage where upstream_db_name = '{dbName}' and upstream_table_name = '{tableName}' and upstream_column_name = '{columnName}' and is_active = 1 and lineage_type != 3  
) tmp 
on c.column_id = tmp.downstream_column_id 
where c.is_active = 1 ;
"""

sql2 = """
    select data_type from column_info where db_name = '{dbName}' and table_name = '{tableName}' and column_name = '{columnName}' and is_active = 1 and meta_type = 0 and sys_id = 2
"""

class PrintData(object):

    @staticmethod
    def print(result,dbName, tableName, columnName, step):
        df1 = SourceDataframe.read_myql("meta",sql1.format(dbName=dbName, tableName=tableName,
                                                           columnName=columnName))
        step = step + 1
        for index, row in df1.iterrows():
            print("第{}层血缘为：".format(step),row["db_name"], row["table_name"], row["column_name"], row["data_type"])
            result.append((step, row["db_name"], row["table_name"], row["column_name"], row["data_type"]))
            PrintData.print(result,row["db_name"],row["table_name"],row["column_name"],step)


if __name__ == '__main__':
    # list = [('ytdw','ods_t_user_d','leave_time')]
    # result = []
    # for item in list:
    #     print("字段：",item, "的下游为：")
    #     temp = SourceDataframe.read_myql("meta", sql2.format(dbName=item[0], tableName=item[1],
    #                                                  columnName=item[2]))
    #     print(temp)
    #     result.append((0, item[0], item[1], item[2], temp.ix[[0]].values[0][0]))
    #     PrintData.print(result,item[0], item[1], item[2], 0)
    # df = pd.DataFrame(result)
    # df.columns = ['层级', '库名', '表名', '字段名', '类型']
    # df.to_excel("result3.xls")

    list= ['dw_order_d',
           'dw_order_tmp1',
           'dwd_area_d',
           'ods_t_area_d',
           'dwd_area_transform_d',
           'dwd_area_d',
           'ods_t_area_d',
           'dwd_enum_info_d',
           'ods_enum_info_d',
           'dwd_gross_profit_d',
           'ods_t_gross_profit_d',
           'dwd_item_batch_history_d',
           'dwd_item_batch_d',
           'ods_t_item_batch_d',
           'dwd_item_batch_spec_d',
           'ods_t_item_batch_spec_d',
           'ods_t_item_batch_history_d',
           'dwd_order_shop_d',
           'ods_pt_order_shop_d',
           'dwd_seller_d',
           'dwd_supplier_carrier_d',
           'ods_t_supplier_carrier_d',
           'dwd_supplier_deposit_d',
           'ods_t_supplier_deposit_d',
           'dwd_supplier_operation_d',
           'ods_t_supplier_operation_d',
           'ods_t_biz_contract_d',
           'ods_t_seller_d',
           'dwd_shop_all_d',
           'ods_t_shop_d',
           'dwd_sp_info_d',
           'ods_t_sp_info_d',
           'dwd_sp_order_snapshot_d',
           'ods_t_sp_order_snapshot_d',
           'dwd_storehouse_d',
           'ods_t_storehouse_d',
           'dwd_trade_shop_d',
           'ods_pt_trade_shop_d',
           'dwd_user_d',
           'ods_t_user_d',
           'dw_item_d',
           'dwd_brand_d',
           'ods_t_brand_d',
           'dwd_enum_info_d',
           'ods_enum_info_d',
           'dwd_item_d',
           'ods_t_item_d',
           'dwd_tag_d',
           'ods_t_tag_d',
           'dw_category_info_d',
           'dwd_category_d',
           'ods_t_category_d',
           'dw_itm_bussiness_group_tag_d',
           'dwd_brand_d',
           'ods_t_brand_d',
           'dwd_business_group_priority',
           'dwd_data_access_d',
           'ods_t_data_access_d',
           'dwd_data_access_detail_d',
           'ods_t_data_access_detail_d',
           'dwd_item_d',
           'ods_t_item_d',
           'dw_itm_pickup_card_d',
           'dwd_brand_d',
           'ods_t_brand_d',
           'dwd_gift_coupon_conf_d',
           'ods_t_gift_coupon_conf_d',
           'dwd_hi_card_template_d',
           'ods_t_hi_card_template_d',
           'dw_category_info_d',
           'dwd_category_d',
           'ods_t_category_d',
           'dw_itm_pickup_card_d',
           'dwd_brand_d',
           'ods_t_brand_d',
           'dwd_gift_coupon_conf_d',
           'ods_t_gift_coupon_conf_d',
           'dwd_hi_card_template_d',
           'ods_t_hi_card_template_d',
           'dw_category_info_d',
           'dwd_category_d',
           'ods_t_category_d',
           'dw_order_after_server_d',
           'dwd_department_d',
           'ods_t_department_d',
           'dwd_enum_info_d',
           'ods_enum_info_d',
           'dwd_job_d',
           'ods_t_job_d',
           'dwd_order_after_server_d',
           'ods_t_order_after_server_d',
           'dwd_server_feature_d',
           'ods_t_server_feature_d',
           'dwd_shop_pool_server_d',
           'ods_t_shop_pool_server_d',
           'dwd_user_d',
           'ods_t_user_d',
           'dw_shop_pool_server_d',
           'dwd_department_d',
           'ods_t_department_d',
           'dwd_enum_info_d',
           'ods_enum_info_d',
           'dwd_job_d',
           'ods_t_job_d',
           'dwd_server_feature_d',
           'ods_t_server_feature_d',
           'dwd_shop_pool_server_d',
           'ods_t_shop_pool_server_d',
           'dwd_user_d',
           'ods_t_user_d',
           'dw_order_tmp2',
           'dwd_account_payable_order_item_d',
           'ods_t_account_payable_order_item_d',
           'dwd_enum_info_d',
           'ods_enum_info_d',
           'dwd_order_item_settle_d',
           'ods_t_order_item_settle_d',
           'ods_t_order_item_settle_increment_d',
           'dwd_order_shop_d',
           'ods_pt_order_shop_d',
           'dwd_settle_order_item_bill_d',
           'ods_t_settle_order_item_bill_d',
           'dwd_settle_original_amount_d',
           'ods_t_settle_original_amount_d',
           'ods_t_settle_original_amount_di',
           'dwd_settle_original_d',
           'ods_t_settle_original_d',
           'dw_order_tmp3',
           'dwd_enum_info_d',
           'ods_enum_info_d',
           'dwd_order_refund_d',
           'ods_t_order_refund_d',
           'dwd_order_shop_d',
           'ods_pt_order_shop_d',
           'dwd_refund_amount_d',
           'ods_t_refund_amount_d',
           'dwd_refund_asset_flow_detail_d',
           'ods_t_refund_asset_flow_detail_d',
           'dwd_refund_logistic_info_d',
           'ods_t_refund_logistic_info_d',
           'dw_order_tmp4',
           'dwd_account_payable_order_item_d',
           'ods_t_account_payable_order_item_d',
           'dwd_coupon_d',
           'dwd_enum_info_d',
           'ods_enum_info_d',
           'ods_t_coupon_d',
           'dwd_coupon_owner_d',
           'ods_t_coupon_owner_d',
           'ods_t_coupon_owner_increment_d',
           'dwd_enum_info_d',
           'ods_enum_info_d',
           'dwd_order_item_settle_extract_d',
           'ods_t_order_item_settle_extract_d',
           'dwd_order_shop_d',
           'ods_pt_order_shop_d',
           'dwd_pt_order_pay_d',
           'ods_pt_order_pay_d',
           'dwd_settle_hi_bill_d',
           'ods_t_settle_hi_bill_d',
           'dwd_settle_hi_overdue_bill_d',
           'ods_t_settle_hi_overdue_bill_d',
           'dwd_settle_order_item_bill_d',
           'ods_t_settle_order_item_bill_d',
           'dwd_settle_original_amount_d',
           'ods_t_settle_original_amount_d',
           'ods_t_settle_original_amount_di',
           'dwd_trade_shop_d',
           'ods_pt_trade_shop_d',
           'dwd_user_group_d',
           'ods_t_user_group_d',
           'dw_item_snapshot_d',
           'dwd_brand_d',
           'ods_t_brand_d',
           'dwd_category_d',
           'ods_t_category_d',
           'dwd_enum_info_d',
           'ods_enum_info_d',
           'dwd_item_snapshot_d',
           'ods_t_item_snapshot_d',
           'dw_trd_pickup_card_category_d',
           'dwd_brand_d',
           'ods_t_brand_d',
           'dwd_card_fund_serial_details_d',
           'ods_t_card_fund_serial_details_d',
           'dwd_hi_card_template_d',
           'ods_t_hi_card_template_d',
           'dw_category_info_d',
           'dwd_category_d',
           'ods_t_category_d']

    print(set(list))
    print(len(set(list)))


