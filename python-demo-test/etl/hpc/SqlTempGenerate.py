import pandas as pd


df1 = pd.read_excel("C:\\Users\\Administrator\\Desktop\\个人\\历史为设置生命周期的表清单 -- 待确认.xlsx")[['库名','表名','拟设置生命周期值']]

sql = "update table_info set life_cycle = {life_cycle}  where db_name = '{db_name}' and table_name = '{table_name}' and meta_type = 0 and is_active = 1;"
for index, row in df1.iterrows():
    db_name = row['库名']
    table_name = row['表名']
    life_cycle = row["拟设置生命周期值"]

    print(sql.format(db_name= db_name, table_name = table_name, life_cycle = life_cycle))