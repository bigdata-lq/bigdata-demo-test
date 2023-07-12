import pandas as pd
import numpy as np
data_test= pd.DataFrame([
    [1,'张三','sex',1],
    [1,'张三','height',1.78],
    [1,'张三','weight',60],
    [2,'李四','sex',1],
    [2,'李四','height',1.75],
    [2,'李四','weight',59],
    [3,'王五','sex',0],
    [3,'王五','height',1.72],
    [3,'王五','weight',58]
    #[3,'王五','weight',58]
],
    columns =['id','name','description','description_value']
)

# print(data_test)

df = data_test.pivot_table(index=['id','name'],#必选参数，用来指定行索引。如果用数组做行索引，数据必须等长
                      columns='description',#必选参数，用来指定列索引。
                      values='description_value'#可选参数，用来做集合的值。默认是显示所有的值。
                      #aggfunc='sum'
                      )

print(df)