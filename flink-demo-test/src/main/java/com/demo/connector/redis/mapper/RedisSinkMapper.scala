package com.demo.connector.redis.mapper

import com.demo.options.RedisSinkProperty
import com.yangt.redis.mapper.{RedisCommand, RedisCommandDescription, RedisMapper}
import org.apache.flink.table.data.{GenericRowData, RowData}

class RedisSinkMapper(redisSinkProperty: RedisSinkProperty) extends RedisMapper[RowData] {

  override def getKeyFromData(rowData: RowData): String = redisSinkProperty.prefix.trim + rowData.asInstanceOf[GenericRowData].getField(0).toString

  override def getValueFromData(rowData: RowData): String = rowData.asInstanceOf[GenericRowData].getField(1).toString

  override def getExpireTime(rowData: RowData): Integer = redisSinkProperty.expireTime

  override def getCommandDescription: RedisCommandDescription = {
    redisSinkProperty.dataType.toLowerCase.trim match {
      case "string" => new RedisCommandDescription(RedisCommand.SET)
      //case "list" => new RedisCommandDescription(RedisCommand.LPUSH)
      case "set" => new RedisCommandDescription(RedisCommand.SADD)
      case _ => throw new Exception("RedisSinkMapper only support 'string' or 'set', not others! ")
    }
  }

}
