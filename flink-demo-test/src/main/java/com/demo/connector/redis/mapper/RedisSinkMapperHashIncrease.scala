package com.demo.connector.redis.mapper

import com.demo.options.RedisSinkProperty
import com.yangt.redis.mapper.{RedisAdditionalMapper, RedisCommand, RedisCommandDescription}
import org.apache.flink.table.data.RowData
import org.apache.flink.types.RowKind

import java.lang

class RedisSinkMapperHashIncrease(redisSinkProperty: RedisSinkProperty) extends RedisAdditionalMapper[RowData]{

  // 对应redis的key
  override def getKeyFromData(rowData: RowData): String = {
    // 仅仅支持定义redis表为string类型（如果需要支持其他类型需单独处理）
    // 此处并没有将RowData 转化为 GenericRowData 因为阿里云flink平台不兼容GenericRowData
    redisSinkProperty.prefix.trim + rowData.getString(0).toString
  }

  // hashMap 中的key 对应的字段
  override def getAdditionalKey(rowData: RowData): String = rowData.getString(1).toString

  // hashMap 中的key 对应value的字段
  override def getValueFromData(rowData: RowData): String = rowData.getString(2).toString


  override def getExpireTime(rowData: RowData): Integer = redisSinkProperty.expireTime

  override def getCommandDescription: RedisCommandDescription = new RedisCommandDescription(RedisCommand.HINCRBY)

  override def isNotDelAdditionalKey(rowData: RowData): lang.Boolean = if (redisSinkProperty.ignoreDelete == false) {
    val rowKind = rowData.getRowKind
    if (rowKind == RowKind.INSERT) {
      return true
    } else if (rowKind == RowKind.DELETE) {
      return false
    } else if (rowKind == RowKind.UPDATE_BEFORE) {
      return false
    } else {
      true
    }
  } else true
}
