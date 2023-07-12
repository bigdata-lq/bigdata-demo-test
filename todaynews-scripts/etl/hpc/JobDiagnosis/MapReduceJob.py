#coding:utf-8
import sys
import json
import time
import requests


TOP_PROCESS_TIME_JOB_NUM=30
YARN_HOST = "http://prod-hadoop-master002"

def get_all_job_base_info():
    """
    :return: 当天yarn执行的所有任务的基本信息
    """
    start_end_timestamp = int(time.time()) * 1000
    start_begin_timestamp = start_end_timestamp - (24 * 60 * 60 * 1000)

    url = YARN_HOST + ":19888/ws/v1/history/mapreduce/jobs?" \
          "startedTimeBegin=%s&startedTimeEnd=%s" % (start_begin_timestamp, start_end_timestamp)
    jobs_base_info = requests.get(url).content
    return jobs_base_info


def get_yarn_job_configuration_info(yarn_job_id):
    """
    Yarn Job Configuration 获取信息
    :return: 返回yarn job query 配置信息
    """
    job_conf_url = YARN_HOST + ":19888/ws/v1/history/mapreduce/jobs/%s/conf" % (yarn_job_id)
    key_property_list = ["mapreduce.job.name", "hive.query.id", "hive.query.string", "mapreduce.job.reduces",
                         "mapreduce.job.maps"]
    job_conf_list = json.loads(requests.get(job_conf_url).content)['conf']['property']

    yarn_job_info_dict = dict()
    for elem in job_conf_list:
        if elem["name"] in key_property_list:
            if elem["name"] == "mapreduce.job.name": # 取Stage-编号
                elem["value"] = elem["value"].split("Stage-")[-1].split(")")[0]
            yarn_job_info_dict[elem["name"]] = elem["value"]
    return yarn_job_info_dict


def get_top_process_time_job(jobs_base_info):
    """
    :return: 执行时间最长的JOB
    """
    jobs_base_list = json.loads(jobs_base_info)["jobs"]["job"]

    job_process_time_dict = dict()
    for job_base_info in jobs_base_list:
        yarn_job_id = job_base_info['id']
        yarn_job_name = job_base_info['name']
        if yarn_job_name.startswith('oozie'):
            continue
        start_time = job_base_info['startTime']
        finish_time = job_base_info['finishTime']
        process_time = (finish_time - start_time) / (1000 * 60) # 单位 分钟
        job_process_time_dict[yarn_job_id] = process_time

    job_sorted_list = sorted(job_process_time_dict.items(), key=lambda d: d[1], reverse=True)[:TOP_PROCESS_TIME_JOB_NUM]
    return job_sorted_list

def get_yarn_job_task_attempt_elaspted_time(yarn_job_id, task_id, successful_attempt):
    """
    Yarn Job Task attempt 的执行时间
    """
    job_task_attempt_url = YARN_HOST + ":19888/ws/v1/history/mapreduce/jobs/%s/tasks/%s/attempts/%s" % (yarn_job_id,task_id,successful_attempt)
    elapsed_time = 0
    try:
        job_task_attempt_info = json.loads(requests.get(job_task_attempt_url).content)['taskAttempt']
        elapsed_time = int(job_task_attempt_info['elapsedTime'] / (1000 * 60))
    except:
        print("can not find taskAttempt id. yarn_job_id: %s  task_id: %s  successful_attempt: %s" % (yarn_job_id,task_id,successful_attempt))
    return elapsed_time

def get_yarn_job_task_info(yarn_job_id):
    """
    Yarn Job Task 获取Map和Reduce执行信息
    :return: Map 和 Reduce task 执行时间
    """
    job_task_url = YARN_HOST + ":19888/ws/v1/history/mapreduce/jobs/%s/tasks" % (yarn_job_id)
    job_task_info_list = json.loads(requests.get(job_task_url).content)['tasks']['task']
    """
    job_task_info_list:
    [
         {
            "progress" : 100,
            "elapsedTime" : 6777,
            "state" : "SUCCEEDED",
            "startTime" : 1326381446541,
            "id" : "task_1326381300833_2_2_m_0",
            "type" : "MAP",
            "successfulAttempt" : "attempt_1326381300833_2_2_m_0_0",
            "finishTime" : 1326381453318
         },
         ...
      ]
    """
    map_elapsed_time_list = list()
    reduce_elapsed_time_list = list()
    for job_task_info in job_task_info_list:
        task_type = job_task_info["type"]
        elapsed_time = int(job_task_info['elapsedTime'] / (1000 * 60))
        task_id = job_task_info['id']
        successful_attempt = job_task_info["successfulAttempt"]
        if task_type == "MAP":
            if len(successful_attempt.split("_")) == 5 or successful_attempt.split("_")[:1] == 0 or successful_attempt == "":
                map_elapsed_time_list.append(elapsed_time)
            else:
                # 有可能出现失败后重试的task，这时候只取执行成功的那一条的 执行时间
                map_elapsed_time_list.append(get_yarn_job_task_attempt_elaspted_time(yarn_job_id, task_id, successful_attempt))
        if task_type == "REDUCE":
            if len(successful_attempt.split("_")) == 5 or successful_attempt.split("_")[:1] == 0 or successful_attempt == "":
                reduce_elapsed_time_list.append(elapsed_time)
        else:
            reduce_elapsed_time_list.append(get_yarn_job_task_attempt_elaspted_time(yarn_job_id, task_id, successful_attempt))
    return map_elapsed_time_list, reduce_elapsed_time_list

def process():
    # step 1. 获取所有Yarn上JOB 基本信息
    jobs_base_info = get_all_job_base_info()
    # step 2. 获取执行时间最长的 JOB列表
    top_process_time_job_list = get_top_process_time_job(jobs_base_info)
    for yarn_job_id, process_time in top_process_time_job_list:
        # step 3. 获取JOB的Task执行时长列表
        map_elapsed_time_list, reduce_elapsed_time_list = get_yarn_job_task_info(yarn_job_id)
        map_num = len(map_elapsed_time_list)
        reduce_num = len(reduce_elapsed_time_list)
        # 找到task列表中 最长执行时间，最短执行时间， 平均执行时间
        map_max_task_time, map_min_task_time, map_avg_task_time, \
        reduce_max_task_time, reduce_min_task_time, reduce_avg_task_time = 0,0,0,0,0,0
        if map_num > 0:
            map_max_task_time = max(map_elapsed_time_list)
            map_min_task_time = min(map_elapsed_time_list)
            map_avg_task_time = sum(map_elapsed_time_list) / len(map_elapsed_time_list)
        if reduce_num > 0:
            reduce_max_task_time = max(reduce_elapsed_time_list)
            reduce_min_task_time = min(reduce_elapsed_time_list)
            reduce_avg_task_time = sum(reduce_elapsed_time_list) / len(reduce_elapsed_time_list)

        # step 4. 找到 查询SQL
        query_sql = ""
        job_conf_dict = get_yarn_job_configuration_info(yarn_job_id)
        if 'hive.query.string' in job_conf_dict:
            query_sql = job_conf_dict['hive.query.string']

        print(yarn_job_id, process_time, query_sql, map_num, map_max_task_time, map_min_task_time, map_avg_task_time, reduce_num, reduce_max_task_time, reduce_min_task_time, reduce_avg_task_time)

if __name__ == "__main__":
    process()
