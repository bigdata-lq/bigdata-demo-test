import os


with open('D:\\code\\code20181219\\alading-bigdata-todaynews\\todaynews-scripts\\etl\\hpc\\data\\hdfs_dir_data.txt','r') as f:
    for line in f:
        if line.rstrip(): ## 去除空格
            hdfs_rm_line = "hdfs dfs -rm -r {path}".format(path = line.rstrip())
            print(hdfs_rm_line)
            # os.system(hdfs_rm_line)



