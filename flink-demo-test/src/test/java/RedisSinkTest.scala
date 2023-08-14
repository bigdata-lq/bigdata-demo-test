import org.apache.flink.streaming.api.scala.StreamExecutionEnvironment
import org.apache.flink.table.api.EnvironmentSettings
import org.apache.flink.table.api.bridge.scala.StreamTableEnvironment
import org.junit.{After, Before, Test}

import java.time.ZoneId

class RedisSinkTest {

  var env: StreamExecutionEnvironment = null
  var settings: EnvironmentSettings = null
  var tEnv: StreamTableEnvironment = null

  @Before
  def before(): Unit ={
    env = StreamExecutionEnvironment.getExecutionEnvironment
    env.setParallelism(2)
    settings = EnvironmentSettings.newInstance().useBlinkPlanner().inStreamingMode().build()
    tEnv = StreamTableEnvironment.create(env, settings)
    val zid = ZoneId.of("Asia/Shanghai")
    tEnv.getConfig.setLocalTimeZone(zid)
  }

  @Test
  def test1(): Unit ={
    val sourceDDL =
      """
        |CREATE TABLE kafka_json_source1 (
        |                            ts BIGINT,
        |                            id INT,
        |                            name VARCHAR
        |                          ) WITH (
        |                            'connector.type' = 'kafka',
        |                            'connector.version' = 'universal',
        |                            'connector.topic' = 'hbtest4',
        |                            'connector.startup-mode' = 'earliest-offset',
        |                            'connector.properties.bootstrap.servers' = 'test-kafka1-idc.yangtuojia.com:9092,test-kafka2-idc.yangtuojia.com:9092',
        |                            'connector.properties.group.id' = 'groupId1',
        |                            'update-mode' = 'append',
        |                            'format.type' = 'json',
        |                            'format.derive-schema' = 'true'
        |                          )
        |""".stripMargin

    val sinkDDL =
      """
        |CREATE TABLE redis_sink1(
        |                            id VARCHAR,
        |                            name VARCHAR,
        |                            city VARCHAR
        |                          ) WITH (
        |                            'connector' = 'yt-redis',
        |                            'yt.connector.host' = 'r-bp12fe59fd823b44.redis.rds.aliyuncs.com',
        |                            'yt.connector.port' = '6379',
        |                            'yt.connector.password' = 'Yangtuojia001',
        |                            'yt.key-prefix' = 'lqtest_',
        |                            'yt.data.type' = 'hash',
        |                            'yt.expire-time' = '300',
        |                            'yt.database' = '6'
        |                          )
        |
        |""".stripMargin

    val sinkDDL2 =
      """
        |CREATE TABLE redis_sink2(
        |                            id VARCHAR,
        |                            city VARCHAR,
        |                            cnt VARCHAR
        |                          ) WITH (
        |                            'connector' = 'yt-redis',
        |                            'yt.connector.host' = 'r-bp12fe59fd823b44.redis.rds.aliyuncs.com',
        |                            'yt.connector.port' = '6379',
        |                            'yt.connector.password' = 'Yangtuojia001',
        |                            'yt.key-prefix' = 'hbtestCC_',
//        |                            'yt.data.type' = 'hash',
        |                            'yt.data.type' = 'hash-increase',
        |                            'yt.expire-time' = '300',
        |                            'yt.database' = '6'
        |                          )
        |
        |""".stripMargin

    val sqlDML = "INSERT INTO redis_sink1 SELECT id, name, 'hz99' AS city FROM kafka_json_source1"
    val sqlDML2 =
      """
        |INSERT INTO redis_sink2
        |SELECT
        |  cast(id as string),
        |  'hz88' AS city,
        |  cast(COUNT(1) as string) AS cnt
        |FROM kafka_json_source1
        |GROUP BY id
        |""".stripMargin

    tEnv.executeSql(sourceDDL)
    tEnv.executeSql(sinkDDL)
    tEnv.executeSql(sinkDDL2)
    //  tEnv.executeSql(sqlDML)
//    tEnv.executeSql("SELECT * from kafka_json_source1").print()
    tEnv.executeSql(sqlDML2)

//    env.execute(this.getClass.getName)
  }

  @After
  def after(): Unit ={
//    tEnv.execute("redis sink方法的测试")
    Thread.sleep(30000)

  }
}
