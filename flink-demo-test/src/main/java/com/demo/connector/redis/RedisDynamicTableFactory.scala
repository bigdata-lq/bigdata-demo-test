package com.demo.connector.redis

import com.demo.options.RedisSinkProperty
import org.apache.flink.configuration.{ConfigOption, ConfigOptions}
import org.apache.flink.table.connector.sink.DynamicTableSink
import org.apache.flink.table.factories.{DynamicTableFactory, DynamicTableSinkFactory, FactoryUtil}
import org.apache.flink.table.types.DataType

import java.util

class RedisDynamicTableFactory extends DynamicTableSinkFactory {
  val HOST = ConfigOptions.key("yt.connector.host").stringType().noDefaultValue()
  val PORT = ConfigOptions.key("yt.connector.port").intType().noDefaultValue()
  val PASSWORD = ConfigOptions.key("yt.connector.password").stringType().noDefaultValue()
  val PREFIX = ConfigOptions.key("yt.key-prefix").stringType().noDefaultValue()
  val DATA_TYPE = ConfigOptions.key("yt.data.type").stringType().noDefaultValue()
  val EXPIRE_TIME = ConfigOptions.key("yt.expire-time").intType().defaultValue(2147483640)
  val DATABASE = ConfigOptions.key("yt.database").intType().defaultValue(0)
  val IGNORE_DELETE = ConfigOptions.key("yt.ignoreDelete").booleanType().defaultValue(true)
  val TABLE_TYPE = ConfigOptions.key("yt.table-type").stringType().defaultValue("sink")

//  val FORMAT = ConfigOptions.key("format").stringType().defaultValue("json") ///


  override def createDynamicTableSink(context: DynamicTableFactory.Context): DynamicTableSink = {
    val helper: FactoryUtil.TableFactoryHelper = FactoryUtil.createTableFactoryHelper(this, context)
//    val encodingFormat: EncodingFormat[SerializationSchema[RowData]] = helper.discoverEncodingFormat(classOf[RetreatJsonFormatFactory], FactoryUtil.FORMAT)  //redis 不需要format
    helper.validate()

    val options = helper.getOptions

    val consumedDataType: DataType = context.getCatalogTable.getSchema.toPhysicalRowDataType()


    val host = options.get(HOST)
    val port = options.get(PORT)
    // 解密
//    val password = AesUtils.aesDecryptNew(options.get(PASSWORD))
    val password = options.get(PASSWORD)
    val prefix = options.get(PREFIX)
    val dataType = options.get(DATA_TYPE)
    val expireTime =  options.get(EXPIRE_TIME)
    val database = options.get(DATABASE)
    val ignoreDelete =  options.get(IGNORE_DELETE)

    val redisProperty = new RedisSinkProperty(host, port, password, prefix, dataType, expireTime, database, ignoreDelete)
    new RedisDynamicTableSink(redisProperty)


  }

  override def factoryIdentifier(): String = "yt-redis"

  override def requiredOptions(): util.Set[ConfigOption[_]] = {
    val set = new util.HashSet[ConfigOption[_]]()
    set.add(HOST)
    set.add(PORT)
    set.add(PREFIX)
    set.add(DATA_TYPE)
    set
  }

  override def optionalOptions(): util.Set[ConfigOption[_]] = {
    val set = new util.HashSet[ConfigOption[_]]()
    set.add(PASSWORD)
    set.add(EXPIRE_TIME)
    set.add(DATABASE)
    set.add(IGNORE_DELETE)
    set.add(TABLE_TYPE)
//    set.add(FORMAT)
    set
  }
}
