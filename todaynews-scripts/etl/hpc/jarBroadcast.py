## -*-coding:utf-8 -*-
#---------
# Name:lq
# Message: jar包广播
# 入参 jar包名称
#---------
import sys
import datetime
import commands

params = sys.argv

hosts =["pre-azkaban001",
        "prod-hirac002"]

uploadShell = """
mv {jarName} {jarName}.bak{nowDay} &&
rz "
"""
scpShell = """
scp /alidata/workspace/rtc_app/flink/{jarName} hadoop@{host}:/alidata/workspace/rtc_app/flink
"""
backShell = """
mv {jarName}.bak{nowDay} {jarName}
"""


if __name__ == '__main__':
    nowDay = datetime.datetime.now().strftime("%Y-%m-%d")
    print('input params is:', str(params))
    result = []
    params.pop(0)
    jarName = params[0]
    retcode, ret = commands.getstatusoutput(uploadShell.format(jarName=jarName, nowDay=nowDay))
    if retcode == 0 :
        for host in hosts:
            commands.getstatusoutput(scpShell.format(jarName=jarName, host=host))
    else:
        print("上传文件失败")
        commands.getstatusoutput(backShell.format(jarName=jarName, nowDay=nowDay))
    print(ret)