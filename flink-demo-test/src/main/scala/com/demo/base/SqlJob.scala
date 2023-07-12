package com.demo.base

import com.demo.udxf._
import com.demo.utils.PropUtil
import org.apache.flink.api.scala._
import org.apache.flink.streaming.api.scala.StreamExecutionEnvironment
import org.apache.flink.table.api.EnvironmentSettings
import org.apache.flink.table.api.bridge.scala.StreamTableEnvironment
import org.apache.flink.types.Row

object SqlJob {


  def main(args: Array[String]): Unit = {
    val env = StreamExecutionEnvironment.getExecutionEnvironment
    val settings: EnvironmentSettings = EnvironmentSettings.newInstance().useBlinkPlanner().inStreamingMode().build()
    val tEnv: StreamTableEnvironment = StreamTableEnvironment.create(env, settings)

//    //用户GMV
//    PropUtil.loadSql("sqls/dayUserGmv.sql")

//    //区域店铺
//    PropUtil.loadSql(path = "sqls/todayAreaShopNew.sql")

    //用户当日订单数
//    PropUtil.loadSql("sqls/dayOrderStaties.sql")

    //当日各区域GMV
//    PropUtil.loadSql("sqls/dayAreaGmv.sql")

    //供应商后台准实时改实时
    PropUtil.loadSql("sqls/dwSettleOrder.sql")

//    PropUtil.loadSql("sqls/adsSettleOrder.sql")
//    PropUtil.loadSql("sqls/dws_settle_indicators.sql")

    val sourceDdls: Array[String] = PropUtil.getProperties("flink.source.ddl").split(";", -1).filter(v => !v.trim.isEmpty)
    val dimDdls: Array[String] = PropUtil.getProperties("flink.dim.ddl").split(";", -1).filter(v => !v.trim.isEmpty)
    val sqls: Array[String] = PropUtil.getProperties("flink.sql").split(";", -1).filter(v => !v.trim.isEmpty && !v.trim.startsWith("--"))

    tEnv.registerFunction("parseJson", new ParseJsonUDF())
    tEnv.registerFunction("jsonHasKey", new JsonHasKeyUDF())
    tEnv.registerFunction("parseBooleanJson", new ParseBooleanJsonUDF())
    tEnv.registerFunction("getItemId", new GetItemId())
    tEnv.registerFunction("haveTag", new HaveTagUDF())
    tEnv.registerFunction("getPromotion", new PromotionAmountUdf())
    tEnv.registerFunction("stringTwoSplit", new StringTwoSplitUDTF())
    tEnv.registerFunction("getTuple", new jsonTupleUDF())
    tEnv.registerFunction("keyValue", new KeyValueUdf())

    for(sourceDdl <- sourceDdls){
      println(sourceDdl)
      tEnv.executeSql(sourceDdl)
    }

    for(dimDdl <- dimDdls){
      tEnv.executeSql(dimDdl)
    }

    for(sql <- sqls){

//      val table: TableResult = tEnv.executeSql(sql)
//      println(table.getTableSchema.toString)
//      println(table.print())
      val table1 = tEnv.sqlQuery(sql)
      table1.printSchema()
      tEnv.toRetractStream[Row](table1).print()

      println("-------------------"+sql+"-------------------------")
    }
    println(env.getExecutionPlan)
    env.execute(this.getClass.getName)

  }

}
