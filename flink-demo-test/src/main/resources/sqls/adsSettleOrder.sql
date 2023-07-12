------
flink.source.ddl =
CREATE TABLE ads_settle_brand_indicators(
    now_day VARCHAR,
    supplier_id VARCHAR,
    brand_id  BIGINT,
    brand_name VARCHAR,
    supplier_gmv BIGINT,
    order_cnt BIGINT,
    shop_cnt BIGINT,
    item_cnt BIGINT,
    proctime AS PROCTIME()
    )
 WITH (
    'connector' = 'kafka',
    'topic' = 'ads_settle_brand_indicators',
    'scan.startup.mode' = 'timestamp',
    'scan.startup.timestamp-millis' = '1598841754000',
    'properties.bootstrap.servers' = '172.16.30.164:9092,172.16.30.165:9092,172.16.30.166:9092,172.16.30.167:9092',
    'properties.group.id' = 'flink.ads_settle_brand_indicators.1',
    'format' = 'json'
 );

 CREATE TABLE ads_settle_shop_indicators(
    now_day VARCHAR,
    supplier_id VARCHAR,
    shop_id  VARCHAR,
    shop_name VARCHAR,
    supplier_gmv BIGINT,
    order_cnt BIGINT,
    shop_cnt BIGINT,
    item_cnt BIGINT,
    proctime AS PROCTIME()
    )
 WITH (
    'connector' = 'kafka',
    'topic' = 'ads_settle_shop_indicators',
    'scan.startup.mode' = 'timestamp',
    'scan.startup.timestamp-millis' = '1598841754000',
    'properties.bootstrap.servers' = '172.16.30.164:9092,172.16.30.165:9092,172.16.30.166:9092,172.16.30.167:9092',
    'properties.group.id' = 'flink.ads_settle_shop_indicators.1',
    'format' = 'json'
 );

 CREATE TABLE ads_settle_province_indicators(
    now_day VARCHAR,
    supplier_id VARCHAR,
    province_id  VARCHAR,
    province_name VARCHAR,
    supplier_gmv BIGINT,
    order_cnt BIGINT,
    shop_cnt BIGINT,
    item_cnt BIGINT,
    proctime AS PROCTIME()
    )
 WITH (
    'connector' = 'kafka',
    'topic' = 'ads_settle_province_indicators',
    'scan.startup.mode' = 'timestamp',
    'scan.startup.timestamp-millis' = '1598841754000',
    'properties.bootstrap.servers' = '172.16.30.164:9092,172.16.30.165:9092,172.16.30.166:9092,172.16.30.167:9092',
    'properties.group.id' = 'flink.ads_settle_province_indicators.1',
    'format' = 'json'
 );

------
flink.dim.ddl =


------
flink.sql =

-- select * from ads_settle_province_indicators;
-- select * from ads_settle_brand_indicators;
select * from ads_settle_shop_indicators;

-- select
-- CONCAT(now_day, '-', supplier_id) only_key,
-- now_day,
-- supplier_id,
-- sum(IF(supplier_gmv IS NULL ,0, supplier_gmv)),
-- sum(IF(order_cnt IS NULL ,0, order_cnt)),
-- sum(IF(shop_cnt IS NULL, 0, shop_cnt)),
-- sum(IF(item_cnt IS NULL, 0, item_cnt))
-- from ads_settle_shop_indicators group by now_day, supplier_id;






------
flink.sink.ddl =