import pandas as pd

valuesFills = ls=[ '%s' for i in range(20)]
print(valuesFills)

# df2 = pd.read_csv(r'6.csv', encoding='utf_8', low_memory=False, names=["file_num","path","table_name"], sep = '\t')
# df1 = pd.read_csv(r'3.csv', encoding='utf_8', low_memory=False, names=["table_name","devoleper","life_cife"])
#
# # print(df1)
# # print(df2)
#
#
# df3 = pd.merge(left=df2, right=df1, how='left',
#                left_on='table_name', right_on='table_name')
#
# # 取没有关联上的部分
# # df3 = df3[df3.isnull().T.any()]
#
# # 保存左关联的结果
# df3.to_csv('表小文件数.csv', header=True, index=True)