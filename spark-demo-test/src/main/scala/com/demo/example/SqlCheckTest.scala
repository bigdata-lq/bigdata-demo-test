package com.demo.example

import org.apache.spark.sql.SparkSession

object SqlCheckTest {
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
        | -- insert overwrite table dwd_meta_type_test
        | select
        | meta_type,count(1) from
        | ytdw.dwd_table_info_d where dayid = '20230329' and is_active = 1 group by meta_type
        |""".stripMargin
    // 去掉注释, 参数替换

    val sessionState = sparkSession.sessionState
    val plan = sessionState.sqlParser.parsePlan(sql1)
    println(plan.toString()) //语法校验&分区判断

    // 禁止删库，删除表，指定队列，禁止insert overwrite
    // 血缘解析参考文档：https://blog.csdn.net/chocolate4/article/details/125561129 实现QueryExecutionListener
    val analyzed = sessionState.executePlan(plan).analyzed  // sql解析，元数据校验 ，血缘解析， 禁止全表扫描
    println(analyzed.toString())

    //遍历树 待访问节点入队列->访问队首节点->子节点再入队列，直到队列空

    //datacenter负载均衡

    sparkSession.close()
  }
}

