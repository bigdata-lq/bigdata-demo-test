------
flink.source.ddl = create table stream_yt_trade_pt_trade_shop_20200602 (
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
    'connector.version'='universal',
    -- 'yt.table-type'='source',
    'connector.topic'='stream_yt_trade_pt_trade_shop_01',
    'connector.properties.max.poll.records'= '200',
    'connector.startup-mode'='earliest-offset',
    'format.derive-schema'='true',
    'connector.type'='kafka',
    'update-mode'='append',
    'connector.properties.bootstrap.servers'='172.16.30.164:9092,172.16.30.165:9092,172.16.30.166:9092,172.16.30.167:9092',
    'connector.properties.group.id'='day_area_shopIds_report_prod_local',
    'format.type'='json'
 );

------
flink.dim.ddl =
CREATE TABLE shop_dim (
	SHOP_ID varchar COMMENT 'ID',
	CITYAREA_ID varchar COMMENT '城市',
	INUSE int
) WITH (
--   'yt.table-type' = 'dim'
  'connector.type' = 'jdbc',
  'connector.url' = 'jdbc:mysql://rm-bp1dyr360ssb1uwnj99.mysql.rds.aliyuncs.com:3306/xxx?useUnicode=true&characterEncoding=utf-8',
  'connector.table' = 't_shop',
  'connector.driver' = 'com.mysql.jdbc.Driver',
  'connector.username' = 'flink', -- optional: jdbc user name and password
  'connector.password' = 'xxx',
  'connector.lookup.cache.max-rows' = '5000000',
  'connector.lookup.cache.ttl' = '259200s',
  'connector.lookup.max-retries' = '3'
);

------
flink.sql =

select
key,
cityarea_id hashKey,
LISTAGG(shop_id_new, ',') hashValue
from
(
    select
    case when type = 'all' then CONCAT('gmvDb',':t_today_area_shop_new:', the_day, ':prod')
         when type = 'b' then CONCAT('gmvDb',':t_today_area_shop_b_new:', the_day, ':prod')
    else CONCAT('gmvDb',':t_today_area_shop_a_new:', the_day, ':prod')
    end as key,
    cityarea_id,
    shop_id_new
    from
    (
        select
        the_day,
        cityarea_id,
        shop_id,
        type,
        shop_id_new,
        flag
        from
        (
            SELECT
              t1.shop_id,
              t2.CITYAREA_ID cityarea_id,
              SUBSTRING(t1.edit_time, 0, 10) the_day,
              haveTag ('30', t1.tags) flag,
              CONCAT(
                CONCAT('all-', shop_id), ':',
                IF(haveTag ('30', t1.tags) = false, CONCAT('a-', shop_id), 'a-'), ':',
                IF(haveTag ('30', t1.tags) = true, CONCAT('b-', shop_id), 'b-')
                ) type_shop_ids
            FROM stream_yt_trade_pt_trade_shop_20200602 t1
            INNER JOIN shop_dim FOR SYSTEM_TIME AS OF t1.proctime AS t2
            ON t1.shop_id = t2.SHOP_ID
            WHERE jsonHasKey(t1._change_column, '"pay_time"') = true and t1.trade_status = 1 and t1.bu_id = 0
            and t2.INUSE = 1
        ) tmp , LATERAL TABLE(stringTwoSplit(type_shop_ids,':', '-')) AS T(type, shop_id_new)
        where shop_id_new <> ''
    ) tmp2
) tmp3 group by key, cityarea_id




------
flink.sink.ddl =