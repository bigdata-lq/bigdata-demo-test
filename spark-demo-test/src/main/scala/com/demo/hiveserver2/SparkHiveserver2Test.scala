package com.demo.hiveserver2

import java.util.Properties

import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.jdbc.JdbcDialects

import scala.collection.mutable.ArrayBuffer

object SparkHiveserver2Test {

  def main(args: Array[String]): Unit = {
    val sparkConf = new SparkConf().setAppName("Spark-Read-Hive-by-scala")
      .setMaster("local[1]");
    val dialect = new HiveSqlDialect() // "" 替换 `  不替换返回的数据也为0
    JdbcDialects.registerDialect(dialect)

    val sparkSession = SparkSession.builder().config(sparkConf).enableHiveSupport().getOrCreate()
    val prop = new Properties()
    prop.put("user", "readonly")
    prop.put("password", "jK01Ctr8VnxIPvj2")
    prop.put("driver", "org.apache.hive.jdbc.HiveDriver")
    prop.put("fetchsize","100") // 默认为 0 , 不设置返回的数据也为0

    val predicates = ArrayBuffer[String]{"dayid = '20221120'"}.toArray
    //    hiveserver2 TD 测试
    val df = sparkSession.read.jdbc("jdbc:hive2://172.16.50.4:10001/ytdw", "dwd_table_info_d", predicates, prop)
    // STS

//    val df = sparkSession.read.jdbc("jdbc:hive2://172.16.50.152:10000/ytdw", "dwd_enum_info_d", predicates, prop)
//    val df = sparkSession.read.jdbc("jdbc:hive2://172.16.50.151:10000/ytdw", "(select enum_key from dwd_enum_info_d where dayid = '20221120' limit 1 ) tmp", prop)
    df.show()

//    Thread.sleep(50000000)
    sparkSession.stop()
  }
}
