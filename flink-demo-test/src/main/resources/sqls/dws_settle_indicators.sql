------
flink.source.ddl =
CREATE TABLE dws_settle_indicators(
    now_day VARCHAR,
    supplier_id VARCHAR,
    supplier_gmv  BIGINT,
    order_cnt BIGINT,
    shop_cnt BIGINT,
    item_cnt BIGINT,
    proctime AS PROCTIME()
    ) WITH (
--     'yt.table-type'='source',
    'connector' = 'kafka',
    'topic' = 'dws_settle_indicators',
    'scan.startup.mode' = 'timestamp',
    'scan.startup.timestamp-millis' = '1601222400000',
    'properties.bootstrap.servers' = '172.16.30.164:9092,172.16.30.165:9092,172.16.30.166:9092,172.16.30.167:9092',
    'properties.group.id' = 'flink.ads_settle_indicators.dev.1',
    'format' = 'json'
 );
------
flink.dim.ddl =


------
flink.sql =
select * from dws_settle_indicators where now_day = '20200928' and supplier_id = '849ad56178e843f5b0e31405011c8f40'




------
flink.sink.ddl =