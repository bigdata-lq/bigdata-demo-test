#!/bin/bash
echo "-------fsimage清除历史数据------"
cd /alidata/setup/hdfs_meta
rm -rf /alidata/setup/hdfs_meta/fsimage_*
rm -rf /alidata/setup/hdfs_meta/data/meta_fsimage_*

echo "-------拉取fsimage数据------"
scp root@prod-hadoop-master001:/alidata/data/dfs/nn/current/fsimage_* /alidata/setup/hdfs_meta
fileList=`ls -l | grep fsimage| grep -v '.md5' | awk '{print $9}' | head -n 1`

hive_load_shell=""

yesterday=`date -d -1days +%Y%m%d`

echo "-------解析fsimage数据------"
for variable in $fileList
do 
        echo "fsimage名称为：${variable}"
        hdfs oiv -i $variable -t /alidata/setup/hdfs_meta/tmp -o /alidata/setup/hdfs_meta/data/meta_${variable}.csv -p Delimited
        sed -i '1d' /alidata/setup/hdfs_meta/data/meta_${variable}.csv

        hive_load_shell+="load data local inpath '/alidata/setup/hdfs_meta/data/meta_${variable}.csv' into table ytdw.ods_hdfs_meta_d partition(dayid='$yesterday');"
done


echo ${hive_load_shell}


echo "-------装载hdfs元数据入hive------"
hive -e "
use ytdw;
create table if not exists ods_hdfs_meta_d
(
    path string comment '目录路径',
    replication string comment '备份数',
    modification_time string comment '最后修改时间',
    access_time  string comment '最后访问时间',
    preferred_block_size string comment '首选块大小(byte)',
    blocks_count string comment '块数',
    file_size  string comment '文件大小(byte)',
    nsquota string comment '名称配额 限制指定目录下允许的文件和目录的数量。',
    dsquota string comment '空间配额 限制该目录下允许的字节数',
    permission string comment '权限',
    user_name tinyint comment '用户',
    group_name  string comment '用户组')
partitioned by (dayid string)
row format delimited fields terminated by '\t'
stored as textfile
location '/dw/ytdw/ods/ods_hdfs_meta_d';

ALTER TABLE ods_hdfs_meta_d DROP IF EXISTS PARTITION (dayid=$yesterday);

$hive_load_shell
;"

echo "-------修改ods_hdfs_meta_d数据为2副本------"
hadoop dfs -setrep -R -w 2 /dw/ytdw/ods/ods_hdfs_meta_d/dayid=$yesterday