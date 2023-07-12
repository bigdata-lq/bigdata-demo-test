------
flink.source.ddl =
CREATE TABLE stream_yt_recon_t_settle_original(
    id BIGINT COMMENT '',
    bill_id BIGINT COMMENT '收入、支出、费用id',
    bu_id INT COMMENT '结算平台 0:海拍客,1:嗨清仓',
    original_id VARCHAR COMMENT '结算元数据id',
    biz_id VARCHAR COMMENT '元数据映射id',
    original_type INT COMMENT '结算数据类型',
    subject_id VARCHAR COMMENT '结算主体id',
    subject_type INT COMMENT '结算主体类型 1:海拍客,2:供应商,3物流商,4:门店',
    settle_type INT COMMENT '结算类型:1:收入、2:支出,3:费用',
    settle_object_id VARCHAR COMMENT '结算对象id',
    settle_object_type INT COMMENT '结算对象类型0:海拍客,1:供应商,2:物流商',
    source_platform INT COMMENT '来源平台(0:海拍客)',
    amount_caliber INT COMMENT '金额结算口径(1, 结算主体给结算对象 2,结算对象给结算主体)',
    settle_amount BIGINT COMMENT '结算金额',
    settle_amount_ex DECIMAL COMMENT '结算金额',
    settle_time VARCHAR COMMENT '结算时间',
    settle_status INT COMMENT '结算状态(0,未结算 1,已结算 2,结算中 3,无需结算)',
    extend_context VARCHAR COMMENT '属性扩展字段',
    is_deleted INT COMMENT '是否删除',
    creator VARCHAR COMMENT '创建人',
    editor VARCHAR COMMENT '修改人',
    create_time VARCHAR COMMENT '创建时间',
    edit_time VARCHAR COMMENT '修改时间',
    filter_tag VARCHAR COMMENT '过滤标识',
    is_syn INT COMMENT '同步标识（0位同步，1已同步，2同步中 ）',
    is_lock INT COMMENT '加锁标识',
    last_lock_time VARCHAR COMMENT '最后锁定时间',
    dc_id INT COMMENT '分销ID',
    _change_column VARCHAR,
    _old_column VARCHAR,
    _ddl_field VARCHAR,
    _table_name VARCHAR,
    _db_name VARCHAR,
    _op_type VARCHAR,
    _execute_time BIGINT,
    proctime AS PROCTIME()
    )
 WITH (
    'connector' = 'kafka',
    'topic' = 'stream_yt_recon_t_settle_original_1',
    'scan.startup.mode' = 'timestamp',
    'scan.startup.timestamp-millis' = '1601210673000',
    'properties.bootstrap.servers' = '172.16.30.164:9092,172.16.30.165:9092,172.16.30.166:9092,172.16.30.167:9092',
    'properties.group.id' = 'flink.settle.test.1',
    'format' = 'json'
 );

 CREATE TABLE stream_yt_recon_t_settle_original_amount (
    id BIGINT COMMENT '自增主键',
    settle_original_id BIGINT  COMMENT '元数据id',
    amount BIGINT COMMENT '结算金额',
    amount_type INT  COMMENT '结算类型',
    amount_desc VARCHAR COMMENT '金额描述',
    amount_caliber INT COMMENT '金额结算口径(1, 结算主体给结算对象 2,结算对象给结算主体)',
    is_settlement INT COMMENT '是否参与结算,0:不参与,1:参与',
    is_deleted INT COMMENT '是否删除',
    creator VARCHAR COMMENT '创建人',
    editor VARCHAR COMMENT '修改人',
    create_time VARCHAR COMMENT '创建时间',
    edit_time VARCHAR COMMENT '修改时间',
    amount_ex DECIMAL COMMENT '结算金额',
    _change_column VARCHAR COMMENT '',
    _old_column VARCHAR COMMENT '',
    _ddl_field VARCHAR COMMENT '',
    _table_name VARCHAR COMMENT '',
    _db_name VARCHAR COMMENT '',
    _op_type VARCHAR COMMENT '',
    _execute_time BIGINT COMMENT '',
    proctime AS PROCTIME()
    )
 WITH (
    'connector' = 'kafka',
    'topic' = 'stream_yt_recon_t_settle_original_amount_1',
    'scan.startup.mode' = 'timestamp',
    'scan.startup.timestamp-millis' = '1601210673000',
    'properties.bootstrap.servers' = '172.16.30.164:9092,172.16.30.165:9092,172.16.30.166:9092,172.16.30.167:9092',
    'properties.group.id' = 'flink.settle.test.1',
    'format' = 'json'
 );

 CREATE TABLE yt_trade_order_trade_shop (
   order_id VARCHAR  COMMENT '主键,订单号',
   trade_id VARCHAR,
   logistic_pay_type TINYINT,
   shop_id VARCHAR,
   shop_name VARCHAR,
   item_id BIGINT,
   item_name VARCHAR,
   brand_id BIGINT,
   brand_name VARCHAR,
   supply_id VARCHAR,
   province_area_id VARCHAR,
   province_area_name VARCHAR,
   pay_time VARCHAR,
   item_count INT,
   bu_id  INT,
   item_dc_id INT,
   proctime AS PROCTIME()
   )
 WITH (
    'connector' = 'kafka',
    'topic' = 'yt_trade_order_trade_shop',
    'scan.startup.mode' = 'timestamp',
    'scan.startup.timestamp-millis' = '1601210673000',
    'properties.bootstrap.servers' = '172.16.30.164:9092,172.16.30.165:9092,172.16.30.166:9092,172.16.30.167:9092',
    'properties.group.id' = 'flink.settle.test.1',
    'format' = 'json'
 );

 CREATE VIEW settle_view AS
SELECT
  b.settle_original_id,
  a.original_id,  -- 订单id
  b.settle_item_amount,
  b.item_logistic_amount,
  b.tax_amount,
  b.packing_amount,
  b.supply_preferential_amount,
  a.proctime
FROM (
  SELECT
    id,
    original_id,
    biz_id,
    proctime
  FROM stream_yt_recon_t_settle_original
  WHERE
    create_time >= '2020-09-25 00:00:00'
    AND bu_id = 0
    AND subject_type = 2   -- 结算主体类型:供应商
    AND original_type = 10 -- 结算数据类型:订单商品行
    AND _op_type = 'INSERT'  -- 只取INSERT的记录
  )a
JOIN(
  SELECT
    settle_original_id,
    SUM(case when amount_type = 7 then amount else 0 end) AS settle_item_amount,
    SUM(case when amount_type = 9 then amount else 0 end) AS item_logistic_amount,
    SUM(case when amount_type = 11 then amount else 0 end) AS tax_amount,
    SUM(case when amount_type = 12 then amount else 0 end) AS packing_amount,
    SUM(case when amount_type in (17,19) then amount else 0 end) AS supply_preferential_amount
  FROM stream_yt_recon_t_settle_original_amount
  WHERE
    create_time >= '2020-09-25 00:00:00'
    AND amount_type in (7,9,11,12,17,19)
    AND _op_type = 'INSERT'   -- 只取INSERT的记录
  GROUP BY settle_original_id
)b
ON a.id = b.settle_original_id
;

-- 结算加上订单维度的宽表
CREATE VIEW settle_order_view AS
SELECT
  b.order_id,
  b.trade_id,
  b.supply_id,
  b.shop_id,
  b.shop_name,
  b.province_area_id AS province_id,
  b.province_area_name AS province_name,
  b.item_id,
  b.item_name,
  b.item_count,
  b.brand_id,
  b.brand_name,
  b.pay_time,
  a.*,
  CASE WHEN b.logistic_pay_type = 1 then a.item_logistic_amount ELSE 0 END AS item_logistic_amount
FROM (
  SELECT
    *
  FROM settle_view
)a
JOIN (
  SELECT
    *
  FROM yt_trade_order_trade_shop
  WHERE pay_time >= '2020-09-25 00:00:00'
)b
ON a.original_id = b.order_id
-- WHERE a.proctime BETWEEN b.proctime - INTERVAL '2' HOUR AND b.proctime + INTERVAL '2' HOUR
;

------
flink.dim.ddl =


------
flink.sql =
select * from (
SELECT
  DATE_FORMAT(TO_TIMESTAMP(pay_time),'yyyyMMdd') AS now_day,
  supply_id AS supplier_id,
  COALESCE(SUM(settle_item_amount + item_logistic_amount + packing_amount + tax_amount - supply_preferential_amount), 0) AS supplier_gmv,  --支付金额（分）,
  COUNT(DISTINCT trade_id) AS order_cnt,
  COUNT(DISTINCT shop_id) AS shop_cnt,
  SUM(item_count) AS item_cnt
FROM settle_order_view
GROUP BY
  DATE_FORMAT(TO_TIMESTAMP(pay_time),'yyyyMMdd'),
  supply_id
  ) tmp where supplier_id = '849ad56178e843f5b0e31405011c8f40'



------
flink.sink.ddl =