import org.apache.flink.streaming.api.scala.StreamExecutionEnvironment
import org.apache.flink.table.api.EnvironmentSettings
import org.apache.flink.table.api.bridge.scala.StreamTableEnvironment
import org.junit.{After, Before, Test}

import java.time.ZoneId

class YtCdcJsonFormatTest {

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
        |CREATE TABLE trade_pt_order_shop (
        |  order_id BIGINT,
        |  trade_id VARCHAR,
        |  bu_id INT,
        |  shop_id VARCHAR,
        |  supply_id VARCHAR,
        |  sku_id BIGINT,
        |  item_id BIGINT,
        |  item_name VARCHAR,
        |  item_count INT,
        |  origin_single_item_amount BIGINT,
        |  pay_amount BIGINT,
        |  tax_amount BIGINT,
        |  item_actual_amount INT,
        |  customer_amount INT,
        |  sharing_amount INT,
        |  logistic_type INT,
        |  logistic_pay_type INT,
        |  logistic_amount BIGINT,
        |  attribute VARCHAR,
        |  spu_feature VARCHAR,
        |  spec INT,
        |  spec_desc VARCHAR,
        |  item_picture VARCHAR,
        |  promotion_attr VARCHAR,
        |  order_status VARCHAR,
        |  refund_status INT,
        |  biz_id BIGINT,
        |  biz_type INT,
        |  out_attr VARCHAR,
        |  bonded_area_id INT,
        |  tags VARCHAR,
        |  accept_time VARCHAR,
        |  pay_time VARCHAR,
        |  stock_out_time VARCHAR,
        |  delivery_time VARCHAR,
        |  end_time VARCHAR,
        |  is_deleted INT,
        |  creator VARCHAR,
        |  editor VARCHAR,
        |  create_time VARCHAR,
        |  edit_time VARCHAR,
        |  _change_column VARCHAR,
        |  _old_column VARCHAR,
        |  _ddl_field VARCHAR,
        |  _table_name VARCHAR,
        |  _db_name VARCHAR,
        |  _op_type VARCHAR,
        |  _execute_time VARCHAR,
        |  proctime AS PROCTIME ()
        |)WITH (
        |  'connector' = 'kafka',
        |  'topic' = 'canal_yt_trade_pt_order_shop',
        |  'properties.bootstrap.servers' = '172.16.30.164:9092,172.16.30.165:9092,172.16.30.166:9092,172.16.30.167:9092',
        |  'properties.group.id' = 'local.flink.order_trade.test.2',
        |  'format' = 'yt-cdc'
        |)
        |
        |""".stripMargin

    tEnv.executeSql(sourceDDL)
    tEnv.executeSql("SELECT * from trade_pt_order_shop limit 100").print()

//    env.execute(this.getClass.getName)
  }

  @After
  def after(): Unit ={
//    tEnv.execute("redis sink方法的测试")
    Thread.sleep(30000)

  }
}
