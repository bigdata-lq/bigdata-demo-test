################# aishangtoutiao.m_news_user_frozen_record #################
create external table if not exists aishangtoutiao.m_news_user_frozen_record (
id int comment '' ,
user_id bigint comment '用户ID' ,
frozen_gold bigint comment '冻结金币数' ,
frozen_balance bigint comment '冻结豆币数' ,
frozen_time timestamp comment '冻结时间' ,
thaw_time timestamp comment '解冻时间' ,
consecutive_days smalint comment '连续未登录天数' ,
advertising_num tinyint comment '解冻广告条数' ,
is_thaw tinyint comment '是否解冻 0 否 1 是' ,
gmt_create timestamp comment '创建时间' ,
gmt_update timestamp comment '更新时间'
)
row format delimited
fields terminated by '\001'
stored as textfile
location '/user/news/mysql/m_news_user_frozen_record';
################# aishangtoutiao.m_news_joke_check_log #################
create external table if not exists aishangtoutiao.m_news_joke_check_log (
id bigint comment '段子审核记录id' ,
joke_id string comment '段子id' ,
subject_name string comment '话题名称' ,
joke_pushtime timestamp comment '段子发布时间' ,
author_id bigint comment '作者id' ,
nick_name string comment '作者昵称' ,
mobile string comment '作者手机号' ,
state tinyint comment '审核状态 0 待审核 ，1 通过 ,2未通过' ,
why string comment '审核不通过原因' ,
admin_id bigint comment '操作人id' ,
admin_name string comment '操作人' ,
gmt_create timestamp comment '创建时间' ,
gmt_update timestamp comment '更新时间' ,
source tinyint comment '来源 1用户 2爬虫 3运营' ,
content string comment '内容' ,
content_source string comment '爬取来源' ,
operator_name string comment '创作人'
)
row format delimited
fields terminated by '\001'
stored as textfile
location '/user/news/mysql/m_news_joke_check_log';
################# aishangtoutiao.m_news_article_check_log #################
create external table if not exists aishangtoutiao.m_news_article_check_log (
id bigint comment '潮闻审核记录id' ,
article_id string comment '潮闻id' ,
subject_name string comment '话题名称' ,
push_date timestamp comment '潮闻发布时间' ,
author_id bigint comment '作者id' ,
nick_name string comment '作者昵称' ,
mobile string comment '作者手机号' ,
state tinyint comment '审核状态 0 待审核 ，1 通过 ,2未通过' ,
why string comment '审核不通过原因' ,
admin_id bigint comment '操作人id' ,
admin_name string comment '操作人' ,
gmt_create timestamp comment '创建时间' ,
gmt_update timestamp comment '更新时间' ,
content string comment '潮闻内容' ,
check_date timestamp comment '审核时间' ,
level_code string comment '频道' ,
operator_name string comment '创作人' ,
source bigint comment '来源 1:用户 2:爬虫 3:运营' ,
content_source string comment '潮闻来源地'
)
row format delimited
fields terminated by '\001'
stored as textfile
location '/user/news/mysql/m_news_article_check_log';
################# aishangtoutiao.m_news_admin_user #################
create external table if not exists aishangtoutiao.m_news_admin_user (
id bigint comment '用户id' ,
username string comment '用户账号' ,
realname string comment '用户名称' ,
password string comment '用户密码' ,
state tinyint comment '状态 0：正常 1：禁用 ' ,
gmt_create timestamp comment '创建时间' ,
gmt_update timestamp comment '更新时间' ,
login_time timestamp comment '最近登入时间' ,
remark string comment '备注' ,
remark1 string comment '备注'
)
row format delimited
fields terminated by '\001'
stored as textfile
location '/user/news/mysql/m_news_admin_user';
################# aishangtoutiao.m_short_video_audit #################
create external table if not exists aishangtoutiao.m_short_video_audit (
video_id bigint comment '视频id' ,
audit_account bigint comment '审核人' ,
audit_type tinyint comment '审核类型 1:手动审核 2:自动审核' ,
audit_status tinyint comment '审核状态: -1不通过 0未审核 1通过 2自动通过' ,
remark string comment '审核不通过理由' ,
create_time timestamp comment '创建时间' ,
update_time timestamp comment '修改时间'
)
row format delimited
fields terminated by '\001'
stored as textfile
location '/user/news/mysql/m_short_video_audit';
