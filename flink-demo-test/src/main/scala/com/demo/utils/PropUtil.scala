package com.demo.utils

import java.util.Properties
import scala.io.Source

object PropUtil {

  val sqlProp = new Properties()

  def loadSql(path: String): Unit ={
    sqlProp.clear()
    val in = Thread.currentThread().getContextClassLoader.getResource(path).openStream()
    val sql = Source.fromInputStream(in).mkString
    println(sql)
    //    val pattern = Pattern.compile("flink([\\s\\S]*?);")
    sql.split("------", -1).filter(v => !v.trim.isEmpty)
        .map(v => {
            val index = v.indexOf("=")
            sqlProp.put(v.substring(0, index).trim, v.substring(index + 1, v.length).trim)
        })
  }

  def getProperties(key: String): String = {
    sqlProp.getProperty(key)
  }

  def main(args: Array[String]): Unit = {
    loadSql("dayUserGmv.sql")
    println(PropUtil.getProperties("flink.source.ddl"))
    println("--------------------------------------------------")
    println(PropUtil.getProperties("flink.sql"))
    println("--------------------------------------------------")
    println(PropUtil.getProperties("flink.dim.ddl"))
//    println(PropUtil.getProperties())
  }

}
