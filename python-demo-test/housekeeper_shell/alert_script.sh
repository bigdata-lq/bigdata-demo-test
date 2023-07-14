#!/bin/bash

OG_ALERT_FILE=$1

date=`date`

# 定义告警日志
ALERT_FILE=/tmp/alert_test.log
# 定义告警解析后日志文件
ALERT_RESULT_FILE=/opt/cloudera/script/alert_result.log

#告警解析存放目录，将原始的告警日志转换为一行行的json存储
TMP_ALERT_FILE=/opt/cloudera/script/tmp_alert.json
cat $OG_ALERT_FILE | jq -r '.[].body.alert|"\(.attributes)"' > $TMP_ALERT_FILE
#sleep 15
echo "Hadoop集群信息通知:\\\\n" > /opt/cloudera/script/ding_text

while read -r line
do
  cluster=$(echo -e $line | jq -r '.CLUSTER_DISPLAY_NAME[]')
  hostname=$(echo -e $line |jq -r '.HOSTS[]')
  if [ $? -ne 0 ];then
     hostname=null
  fi
  echo -e $line | jq -r '.|"\(.HEALTH_TEST_RESULTS[])"' |while read alert; do
    alert_service=$(echo -e $alert | jq -r '.testName')
    alert_enent_doce=$(echo -e $alert | jq -r '.code')
    alert_content=$(echo -e $alert | jq -r '.content')
    alert_severity=$(echo -e $alert | jq -r '.severity')
    echo "告警集群:[$cluster],告警主机：[$hostname],告警级别：[$alert_severity],告警服务:[$alert_service],告警事件编码:[$alert_enent_doce],告警详细内容：[$alert_content]" >> $ALERT_RESULT_FILE
    if [[ $alert_severity =~ "CRITICAL" ]];
    then 
	ding_detail="告警集群:[$cluster]\\\\n告警主机:[$hostname]\\\\n告警级别:[$alert_severity]\\\\n告警服务:[$alert_service]"
	echo $ding_detail >> /opt/cloudera/script/ding_text
    fi
  done

done < $TMP_ALERT_FILE
#sleep 10
ding_text=$(cat /opt/cloudera/script/ding_text |sed  's/^/\\\\n/' |awk BEGIN{RS=EOF}'{gsub(/\n/,"");print}')
echo $ding_text
#发送钉钉告警消息
if [[ $ding_text =~ "CRITICAL" ]];
then
	echo $ding_text
	ssh hadoop@172.16.50.27 "export JAVA_HOME=/alidata/server/java;sh /home/hadoop/alarm/ding/ding.sh $ding_text "
fi

if [[ $ding_text =~ "CRITICAL" ]];
then
    if [[ $ding_text =~ "[hcluster]" || $ding_text =~ "HBase-Prod-PP" || $ding_text =~ "hcluster-prod-streaming" ]];
    then
        ssh hadoop@172.16.50.27 "export JAVA_HOME=/alidata/server/java;python3 /home/hadoop/alarm/phone/AlertTelPhone.py "
    fi
fi
echo "$date: Wrting log to $ALERT_RESULT_FILE" >> $ALERT_FILE
