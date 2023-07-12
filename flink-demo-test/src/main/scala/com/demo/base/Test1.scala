package com.demo.base

import org.apache.flink.streaming.api.scala.StreamExecutionEnvironment
import org.apache.flink.table.api.EnvironmentSettings
import org.apache.flink.table.api.bridge.scala.StreamTableEnvironment

import java.time.{Instant, ZoneId}
import java.util.TimeZone

object Test1 extends App {

  println("tz: "+System.getProperty("user.timezone"))

  // 会起作用的
  //System.setProperty("user.timezone", "America/St_Johns")
  //TimeZone.setDefault(TimeZone.getTimeZone("America/St_Johns"))

  val env = StreamExecutionEnvironment.getExecutionEnvironment
  env.setParallelism(2)

  println("tz: "+System.getProperty("user.timezone"))


  val settings: EnvironmentSettings = EnvironmentSettings.newInstance().useBlinkPlanner().inStreamingMode().build()
  val tEnv: StreamTableEnvironment = StreamTableEnvironment.create(env, settings)

  //val tz = TimeZone.getTimeZone("Asia/Shanghai")
  val zid = ZoneId.of("Asia/Shanghai")
  //val zid = ZoneId.of("America/St_Johns")
  tEnv.getConfig.setLocalTimeZone(zid)

  val tz = TimeZone.getDefault
  println(tz)
  val  now = Instant.now()
  println(now)




  //val source = env.fromElements("a", "b")

  val sourceDDL =
    """
      |
      |create table kafka_json_source1(
      |                            ts BIGINT,
      |                            id int,
      |                            name varchar,
      |                            proctime as PROCTIME(),
      |                            rowtime as TO_TIMESTAMP(FROM_UNIXTIME(ts/1000,'yyyy-MM-dd HH:mm:ss')),
      |                            WATERMARK FOR rowtime AS rowtime - INTERVAL '1' SECOND,
      |                            lt as LOCALTIMESTAMP
      |
      |                          ) with (
      |                            'connector.type' = 'kafka',
      |                            'connector.version' = 'universal',
      |                            'connector.topic' = 'hbtest4',
      |                            'connector.startup-mode' = 'earliest-offset',
      |                            'connector.properties.zookeeper.connect' = '172.16.50.34:2181,172.16.50.39:2181',
      |                            'connector.properties.bootstrap.servers' = '172.16.50.47:9092,172.16.50.46:9092',
      |                            'connector.properties.group.id' = 'groupId1',
      |                            'update-mode' = 'append',
      |                            'format.type' = 'json',
      |                            'format.derive-schema' = 'true'
      |
      |                          )
      |
      |
      |
      |""".stripMargin

  tEnv.sqlUpdate(sourceDDL)

  tEnv.from("kafka_json_source1").printSchema()

  val sql1 = """select * , proctime  as p2 from kafka_json_source1 """

  val sql2 = """select name, count(name) , TIMESTAMPADD( hour,8,TUMBLE_START(proctime, INTERVAL '3' SECOND) )as wstart from kafka_json_source1 group by TUMBLE(proctime, INTERVAL '3' SECOND), name"""

  val sql3 = """select name, count(name) , TUMBLE_START(rowtime, INTERVAL '10' SECOND) as wstart from kafka_json_source1 group by TUMBLE(rowtime, INTERVAL '10' SECOND), name"""


  tEnv.executeSql(sql2).print()


  //source.print()

  env.execute()


}

