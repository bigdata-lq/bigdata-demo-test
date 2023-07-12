################# 新闻app金额金币报表 #################
create external table if not exists aishangtoutiao.r_news_payment_report (
day_time date comment '时间',
wind_type string comment '风控状态',
balance double comment '总金额（冻结和非冻结）',
gold double comment '总金币（冻结和非冻结）',
no_frozen_balance double comment '总金额（非冻结）',
no_frozen_gold double comment '总金币（非冻结）',
all_num bigint  comment '总人数（冻结和非冻结）',
no_frozen_num bigint  comment '总人数（非冻结）'
)
row format delimited
fields terminated by '\001'
stored as textfile
location '/user/news/pm/news_payment_report';