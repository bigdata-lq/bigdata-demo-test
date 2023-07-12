------
flink.source.ddl =
create table stream_yt_trade_pt_order_shop_01 (
id BIGINT,
order_id BIGINT,
order_no VARCHAR,
trade_id VARCHAR,
bu_id INT,
shop_id VARCHAR,
supply_id VARCHAR,
sku_id BIGINT,
item_id BIGINT,
item_name VARCHAR,
item_count INT,
origin_single_item_amount BIGINT,
pay_amount BIGINT,
tax_amount BIGINT,
item_actual_amount INT,
customer_amount INT,
sharing_amount INT,
logistic_type INT,
logistic_pay_type INT,
logistic_amount BIGINT,
attribute VARCHAR,
spu_feature VARCHAR,
spec INT,
spec_desc VARCHAR,
item_picture VARCHAR,
promotion_attr VARCHAR,
order_status VARCHAR,
refund_status INT,
biz_id BIGINT,
biz_type INT,
out_attr VARCHAR,
bonded_area_id INT,
tags VARCHAR,
accept_time VARCHAR,
pay_time VARCHAR,
stock_out_time VARCHAR,
delivery_time VARCHAR,
end_time VARCHAR,
is_deleted INT,
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
'connector.properties.zookeeper.connect'='172.16.30.11:2181 172.16.30.12:2181 172.16.30.13:2181',
'connector.version'='universal',
'connector.topic'='stream_yt_trade_pt_order_shop_01',
'connector.startup-mode' = 'earliest-offset',
'format.derive-schema'='true',
'connector.type'='kafka',
'update-mode'='append',
'connector.properties.bootstrap.servers'='172.16.30.164:9092,172.16.30.165:9092,172.16.30.166:9092,172.16.30.167:9092',
'connector.properties.group.id'='flink.trade.order.20200618',
'connector.properties.max.poll.records'= '200',
'connector.properties.max.poll.interval.ms'= '600000',
'format.type'='json'
 );
------
flink.dim.ddl =

------
flink.sql =
select
*
from
stream_yt_trade_pt_order_shop_01


-- -- 类目购买订单集合(order_id)
-- INSERT INTO redis_set_sink1
-- SELECT
--   CONCAT('reco_rt:',the_day, ':', 'rt:feature:shop5cate', ':cnt_cate_order:', shop_id, ':', CAST(category as VARCHAR))  AS  setKey,
--   order_id AS setValue
-- FROM (
--   SELECT
--     shop_id,
--     category,
--     DATE_FORMAT(TO_TIMESTAMP(pay_time),'yyyyMMdd') AS the_day,
--     order_id
--   FROM (
--     SELECT
--       t1._change_column AS f0,
--       t1.*,
--       t2.brand,
--       t2.category
--     FROM stream_yt_trade_pt_order_shop_01 t1
--     LEFT JOIN item_dim  FOR SYSTEM_TIME AS OF t1.proctime AS t2
--     ON t1.item_id = t2.id
--     WHERE jsonHasKey(t1._change_column, '"pay_time"') = true and t2.category is not null
-- 	AND DATE_FORMAT(TO_TIMESTAMP(t1.pay_time),'yyyyMMdd') > '20200620'
--   ) o
-- ) a ;
--
-- -- 品牌购买订单集合(order_id)
--
-- INSERT INTO redis_set_sink1
-- SELECT
--   CONCAT('reco_rt:', the_day, ':', 'rt:feature:shop5brand', ':cnt_brand_order:', shop_id, ':', CAST(brand as VARCHAR)) AS setKey,
--   order_id AS setValue
-- FROM (
--   SELECT
--     shop_id,
--     brand,
--     DATE_FORMAT(TO_TIMESTAMP(pay_time),'yyyyMMdd') AS the_day,
--     order_id
--   FROM (
--     SELECT
--       t1._change_column AS f0,
--       t1.*,
--       t2.brand,
--       t2.category
--     FROM stream_yt_trade_pt_order_shop_01 t1
--     LEFT JOIN item_dim  FOR SYSTEM_TIME AS OF t1.proctime AS t2
--     ON t1.item_id = t2.id
--     WHERE jsonHasKey(t1._change_column, '"pay_time"') = true and t2.brand is not null
-- 	AND DATE_FORMAT(TO_TIMESTAMP(t1.pay_time),'yyyyMMdd') > '20200620'
--   ) o
-- ) a ;
--
-- -- 当日购买贸易集合(trade_id)
-- INSERT INTO redis_set_sink2
-- SELECT
--   CONCAT('reco_rt:', the_day, ':', 'rt:feature:shop', ':cnt_shop_order:', shop_id) AS setKey,
--   trade_id AS setValue
-- FROM (
--   SELECT
--     shop_id,
--     DATE_FORMAT(TO_TIMESTAMP(pay_time),'yyyyMMdd') AS the_day,
--     trade_id
--   FROM (
--     SELECT
--       t1.*
--     FROM stream_yt_trade_pt_order_shop_01 t1
--     WHERE jsonHasKey(t1._change_column, '"pay_time"') = true
-- 	AND DATE_FORMAT(TO_TIMESTAMP(t1.pay_time),'yyyyMMdd') > '20200620'
--   ) o
-- ) a ;
--
-- -- 当日购买商品集合(全量)
-- INSERT INTO redis_set_sink1
-- SELECT
--   CONCAT('reco_rt:', the_day, ':', 'rt:trace', ':', 'item_ids_all', ':', shop_id) AS setKey,
--   item_id AS setValue
--   FROM (
--     SELECT
--       shop_id,
--       DATE_FORMAT(TO_TIMESTAMP(pay_time),'yyyyMMdd') AS the_day,
--       item_id
--     FROM stream_yt_trade_pt_order_shop_01 t1
--     WHERE jsonHasKey(t1._change_column, '"pay_time"') = true
-- 	AND DATE_FORMAT(TO_TIMESTAMP(t1.pay_time),'yyyyMMdd') > '20200620'
--   ) o ;
--
--
--
-- -- 当日购买过的商品集合
-- INSERT INTO redis_set_sink1
-- SELECT
--   CONCAT('reco_rt:', the_day, ':', 'rt:trace', ':', 'item_ids_ordered', ':', shop_id) AS setKey,
--   item_id AS setValue
--   FROM (
--     SELECT
--       shop_id,
--       DATE_FORMAT(TO_TIMESTAMP(pay_time),'yyyyMMdd') AS the_day,
--       item_id
--     FROM stream_yt_trade_pt_order_shop_01 t1
--     WHERE jsonHasKey(t1._change_column, '"pay_time"') = true
-- 	AND DATE_FORMAT(TO_TIMESTAMP(t1.pay_time),'yyyyMMdd') > '20200620'
--   ) o ;
--
--
-- -- 用户购买的商品订单集合(order_id)
-- INSERT INTO redis_set_sink1
-- SELECT
--   CONCAT('reco_rt:', the_day, ':', 'rt:feature:shop5item', ':cnt_order:', shop_id, ':', CAST(item_id as VARCHAR)) AS setKey,
--   order_id AS setValue
-- FROM (
--   SELECT
--     shop_id,
--     item_id,
--     DATE_FORMAT(TO_TIMESTAMP(pay_time),'yyyyMMdd') AS the_day,
--     order_id
--   FROM (
--     SELECT
--       t1.*
--     FROM stream_yt_trade_pt_order_shop_01 t1
--     WHERE jsonHasKey(t1._change_column, '"pay_time"') = true and t1.shop_id is not null and t1.item_id is not null
-- 	AND DATE_FORMAT(TO_TIMESTAMP(t1.pay_time),'yyyyMMdd') > '20200620'
--   ) o
-- ) a ;

















------
flink.sink.ddl =

