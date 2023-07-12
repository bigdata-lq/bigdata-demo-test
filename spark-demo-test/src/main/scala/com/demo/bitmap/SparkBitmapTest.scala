package com.demo.bitmap

import org.apache.spark.sql.SparkSession

object SparkBitmapTest {

  def main(args: Array[String]): Unit = {
    val sparkSession: SparkSession = SparkSession
      .builder()
      .appName("Java Spark Hive Example")
      .master("local[*]")
      .config("spark.sql.warehouse.dir", "hdfs://user/hive/warehouse")
      .config("driver","com.mysql.jdbc.Driver")
      .enableHiveSupport()
      .getOrCreate()

//    sparkSession.sql("show databases").show()

    val sql1 =
      """
        | select meta_type, count(dintict table_name) from
        | dwd_table_info_d where dayid = '20230329' and is_active = 1 group by meta_type
        |""".stripMargin
    sparkSession.sql("use ytdw")
    val dataFrame = sparkSession.sql(sql1)
    dataFrame.show(true)

    sparkSession.close()
  }

}
