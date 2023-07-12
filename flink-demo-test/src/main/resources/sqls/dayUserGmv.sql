------
flink.source.ddl =
create table stream_yt_trade_pt_trade_shop_01 (
id BIGINT,
trade_id VARCHAR,
trade_no VARCHAR,
parent_trade_id VARCHAR,
out_trade_id VARCHAR,
bu_id INT,
item_dc_id INT,
shop_id VARCHAR,
buyer_user_id VARCHAR,
supply_id VARCHAR,
store_id BIGINT,
parent_shop_id VARCHAR,
user_id VARCHAR,
open_id VARCHAR,
third_order_time VARCHAR,
trade_type TINYINT,
trade_source TINYINT,
trade_from VARCHAR,
trade_status TINYINT,
pay_amount BIGINT,
logistic_amount BIGINT,
logistic_pay_type TINYINT,
trade_remark VARCHAR,
shop_remark VARCHAR,
clerk_name VARCHAR,
clerk_phone VARCHAR,
address_id BIGINT,
area_id VARCHAR,
city_area_id VARCHAR,
province_area_id VARCHAR,
delivery_name VARCHAR,
delivery_phone VARCHAR,
detail_address VARCHAR,
customer_id VARCHAR,
customer_id_card VARCHAR,
customer_name VARCHAR,
customer_phone VARCHAR,
tags VARCHAR,
is_cart TINYINT,
attribute VARCHAR,
promotion_attr VARCHAR,
has_parent TINYINT,
hide TINYINT,
pay_time VARCHAR,
end_time VARCHAR,
is_deleted TINYINT,
creator VARCHAR,
editor VARCHAR,
create_time VARCHAR,
edit_time VARCHAR,
_change_column VARCHAR,
_old_column VARCHAR,
_ddl_field VARCHAR,
_table_name VARCHAR,
_db_name VARCHAR,
_op_type VARCHAR,
_execute_time BIGINT,
proctime AS PROCTIME ()
)
 with (
'connector.properties.max.poll.records'= '200',
'connector.properties.max.poll.interval.ms'= '600000',
'connector.version'='universal',
-- 'yt.table-type'='source',
'connector.topic'='stream_yt_trade_pt_trade_shop_01',
'connector.startup-mode'='earliest-offset',
'format.derive-schema'='true',
'connector.type'='kafka',
'update-mode'='append',
'connector.properties.bootstrap.servers'='172.16.30.164:9092,172.16.30.165:9092,172.16.30.166:9092,172.16.30.167:9092',
'connector.properties.group.id'='day_user_gmv_report_lq_test111',
'format.type'='json'
 );

------
flink.dim.ddl =
CREATE TABLE shop_dim (
	SHOP_ID varchar COMMENT 'ID',
	store_type int COMMENT '门店类型 1 母婴 2 港货/进口 3 美妆 4 药店 5 商超 6 便利店 7 线上 8 其他 9 员工店 10 二批商 11pp',
	INUSE int COMMENT '是否有效'
) WITH (
  -- 'yt.table-type' = 'dim',
  'connector.type' = 'jdbc',
  'connector.url' = 'jdbc:mysql://rm-bp1dyr360bss1uwnj99.mysql.rds.aliyuncs.com:3306/xxx?useUnicode=true&characterEncoding=utf-8',  -- 使用pdb来替代
  'connector.table' = 't_shop',
  'connector.driver' = 'com.mysql.jdbc.Driver',
  'connector.username' = 'flink', -- optional: jdbc user name and password
  'connector.password' = 'xxx'
  -- 'connector.lookup.cache.max-rows' = '200000',
  -- 'connector.lookup.cache.ttl' = '259200s',
  -- 'connector.lookup.max-retries' = '3'
);

CREATE TABLE shop_pool_server_dim (
	shop_id varchar COMMENT '门店ID',
	user_id varchar COMMENT '用户ID',
	is_enabled boolean,
	is_deleted boolean
) WITH (
  -- 'yt.table-type' = 'dim',
  'connector.type' = 'jdbc',
  'connector.url' = 'jdbc:mysql://rm-bp1dyr360bss1uwnj99.mysql.rds.aliyuncs.com:3306/xxx?useUnicode=true&characterEncoding=utf-8',  -- 使用pdb来替代
  'connector.table' = 't_shop_pool_server',
  'connector.driver' = 'com.mysql.jdbc.Driver',
  'connector.username' = 'flink',
  'connector.password' = 'xxx'
  -- 'connector.lookup.cache.max-rows' = '200000',
  -- 'connector.lookup.cache.ttl' = '259200s',
  -- 'connector.lookup.max-retries' = '3'
);

------
flink.sql =
select
    CONCAT(DATE_FORMAT(TO_TIMESTAMP(edit_time),'yyyyMMdd'), '-', after_server_id) only_key,
    after_server_id as user_id,
    cast(DATE_FORMAT(TO_TIMESTAMP(edit_time),'yyyyMMdd') as bigint) as now_day,
    sum(case when trade_type = '1' then gmv else 0 end) as hi_gmv,
    sum(case when trade_type <> '1' and tg=false then gmv else 0 end) as a_gmv,
    sum(case when trade_type <> '1' and tg=true and crms = false then gmv else 0 end) as b_gmv,
    sum(gmv) as all_gmv,
    count(distinct shop_id) as shop_count
from
(
    select
    after_server_id,
    trade_id,
    trade_no,
    shop_id,
    edit_time,
    pay_amount + cast(if(getPromotion(6, promotion_attr) is null,0,getPromotion(6, promotion_attr)) as bigint) as gmv,
    cast(trade_type as string)  as trade_type,
    haveTag('30', tags)  as tg,
    haveTag('39', tags)  as crms,
    row_num
    from
    (
    SELECT
      t1.*,
      t2.store_type,
      t2.INUSE,
      t3.user_id as after_server_id,
      t1._change_column,
      ROW_NUMBER() OVER (PARTITION BY t1.trade_no, t3.user_id ORDER BY t1.proctime ASC) as row_num
    FROM stream_yt_trade_pt_trade_shop_01 t1
    INNER JOIN shop_dim FOR SYSTEM_TIME AS OF t1.proctime AS t2
    ON t1.shop_id = t2.SHOP_ID
    INNER JOIN shop_pool_server_dim FOR SYSTEM_TIME AS OF t1.proctime AS t3
    ON t1.shop_id = t3.shop_id
    WHERE jsonHasKey(t1._change_column, '"pay_time"') = true and
    jsonHasKey(t1._change_column, '"trade_status":"1"') = true and t1.bu_id = 0 and t1.item_dc_id = 0
    and t3.is_enabled = false AND t3.is_deleted = false
    and t2.store_type <> 9 and t2.INUSE = 1
    AND DATE_FORMAT(TO_TIMESTAMP(t1.edit_time),'yyyyMMdd') >= '20200803'
    ) tmp1 where row_num = 1
)  tmp2 group by DATE_FORMAT(TO_TIMESTAMP(edit_time),'yyyyMMdd'), after_server_id;




------
flink.sink.ddl =