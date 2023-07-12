## -*-coding:utf-8 -*-
#-------------------------------------------------------------------------------
# Name:lq
# Message: 基础日期信息 特定生成日期方法
#-------------------------------------------------------------------------------

import datetime

class Param(object):

    def __init__(self, dicts= {}, dayNum= 0):
        now_day = datetime.datetime.now() + datetime.timedelta(days=-dayNum)
        one_days_before = now_day + datetime.timedelta(-1)
        three_days_before = now_day + datetime.timedelta(-3)
        seven_days_before = now_day + datetime.timedelta(-7)

        dicts['ARG_TODAY_ISO'] = now_day.strftime("%Y-%m-%d") #yyyy-mm-dd 当天
        dicts['ARG_TODAY_ISO_1'] = one_days_before.strftime("%Y-%m-%d") # yyyy-mm-dd 一天前
        dicts['ARG_TODAY_ISO_DAY_3'] = three_days_before.strftime("%Y-%m-%d") # yyyy-mm-dd 三天前
        dicts['ARG_TODAY_ISO_DAY_7'] = seven_days_before.strftime("%Y-%m-%d") # yyyy-mm-dd 七天前

        ### 上周，本周，下周的第一天
        dicts['ARG_TODAY_LAST_WEEK_START'] = (now_day - datetime.timedelta(days=now_day.weekday()+7)).strftime("%Y-%m-%d")
        dicts['ARG_TODAY_WEEK_START'] = (now_day - datetime.timedelta(days=now_day.weekday())).strftime("%Y-%m-%d")
        dicts['ARG_TODAY_NEXT_WEEK_START'] = (now_day - datetime.timedelta(days=now_day.weekday()-7)).strftime("%Y-%m-%d")

        ### 上周，本周，下周的最后一天
        dicts['ARG_TODAY_LAST_WEEK_END'] = (now_day - datetime.timedelta(days=now_day.weekday()+1)).strftime("%Y-%m-%d")
        dicts['ARG_TODAY_THIS_WEEK_END'] = (now_day + datetime.timedelta(days=6-now_day.weekday())).strftime("%Y-%m-%d")
        dicts['ARG_TODAY_NEXT_WEEK_END'] = (now_day + datetime.timedelta(days=13-now_day.weekday())).strftime("%Y-%m-%d")

        ### 上月第一天和最后一天
        dicts['ARG_TODAY_LAST_MOUTH_START'] = datetime.date(datetime.date.today().year,datetime.date.today().month-1,1).strftime("%Y-%m-%d")
        dicts['ARG_TODAY_LAST_MOUTH_END'] = (datetime.date(datetime.date.today().year,datetime.date.today().month,1)-datetime.timedelta(1)).strftime("%Y-%m-%d")

        ### 本月第一天
        dicts['ARG_TODAY_THIS_MOUTH_START'] = datetime.date(datetime.date.today().year,datetime.date.today().month,1).strftime("%Y-%m-%d")

        self.dicts = dicts

    @staticmethod
    def get_last_day(num = 0):

        """
        num:选择天数
        获取某天开始时间或者结束时间
        """
        dicts = {}
        one_day = datetime.datetime.now() + datetime.timedelta(days=-num)
        one_days_before = one_day + datetime.timedelta(-1)
        dicts['ARG_TODAY_START'] = one_days_before.strftime("%Y-%m-%d")
        dicts['ARG_TODAY_END'] =  one_day.strftime("%Y-%m-%d")
        return dicts