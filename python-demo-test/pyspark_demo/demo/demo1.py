from pyspark.sql import SparkSession
from datetime import datetime, date
import time


spark = SparkSession.builder.getOrCreate()
conf = spark.conf
conf.set("spark.executor.cores","4")



df = spark.createDataFrame([
    (1, 2., 'string1', date(2000, 1, 1), datetime(2000, 1, 1, 12, 0)),
    (2, 3., 'string2', date(2000, 2, 1), datetime(2000, 1, 2, 12, 0)),
    (3, 4., 'string3', date(2000, 3, 1), datetime(2000, 1, 3, 12, 0))
], schema='a long, b double, c string, d date, e timestamp')

tmp_table="t_test_1"

df.createGlobalTempView(tmp_table)
df2 = spark.sql("""
select * from global_temp.{tmp_table}
""".format(tmp_table = tmp_table)).drop("a").repartition()
df2.persist()

df2.show(20)

time.sleep(1800)

spark.stop()