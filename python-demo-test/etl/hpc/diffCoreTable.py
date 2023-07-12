## -*-coding:utf-8 -*-
#---------
# Name:lq
# Message: 比较核心表之间的差距
# 入参 downstream ytdw dw_order_d order_id
#---------
import sys
import pandas as pd


df1 = pd.read_csv("C:\\Users\\Administrator\\Downloads\\coreTables-2021-01-01.csv")['table_name'].tolist()

df2 = pd.read_csv("C:\\Users\\Administrator\\Downloads\\coreTables-2021-01-02.csv")['table_name'].tolist()

df3 = pd.read_csv("C:\\Users\\Administrator\\Downloads\\coreTables-2021-01-04.csv")['table_name'].tolist()

print(list(set(df1).difference(set(df2))))

print(list(set(df1).difference(set(df3))))