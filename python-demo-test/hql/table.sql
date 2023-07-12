############每日新增设备记录表################
create external table if not exists aishangtoutiao.r_todaynews_new_device (
mon_time string   COMMENT '月时间',
week_time string  COMMENT '周时间',
day_time string  COMMENT '天时间',
deviceid string   COMMENT '设备号',
channel string   COMMENT '渠道'
)
stored as PARQUET
location '/user/news/data/new_res';

############每日新增设备记录表################
CREATE EXTERNAL TABLE `m_news_app_pv`(
  `day_time` string COMMENT '时间',
  `view` string COMMENT '曝光量',
  `cw_pv` string COMMENT '潮闻pv',
  `sv_pv` string COMMENT '小视频pv',
  `ggj_pv` string COMMENT '咕咕鸡pv',
  `click` string COMMENT '点击量')
LOCATION 'hdfs://nameservice1/user/news/mysql/news_app_pv'

############ 用户余额、金币报表 ############
create external table if not exists aishangtoutiao.r_news_app_payment_report (
date date comment '日期时间'
wind_type string comment '风控状态'
balance double comment '总金额（冻结和非冻结）'
gold double comment '总金币（冻结和非冻结）'
no_frozen_balance double comment '总金额（非冻结）'
no_frozen_gold double comment '总金币（非冻结）'
all_num long comment '总人数（冻结和非冻结）'
no_frozen_num long comment '总人数（非冻结）'
)
row format delimited
fields terminated by '\001'
stored as textfile
location '/user/news/pm/news_app_payment_report';



