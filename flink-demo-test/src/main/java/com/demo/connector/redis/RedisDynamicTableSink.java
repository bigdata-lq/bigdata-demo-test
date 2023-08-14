package com.demo.connector.redis;


import com.demo.connector.redis.mapper.RedisSinkMapper;
import com.demo.connector.redis.mapper.RedisSinkMapperHash;
import com.demo.connector.redis.mapper.RedisSinkMapperHashIncrease;
import com.demo.connector.redis.mapper.RedisSinkMapperZSET;
import com.demo.options.RedisSinkProperty;
import com.yangt.redis.config.FlinkJedisPoolConfig;
import org.apache.flink.table.connector.ChangelogMode;
import org.apache.flink.table.connector.sink.DynamicTableSink;
import org.apache.flink.table.connector.sink.SinkFunctionProvider;
import org.apache.flink.types.RowKind;

public class RedisDynamicTableSink implements DynamicTableSink {


    private RedisSinkProperty redisSinkProperty;

    public RedisDynamicTableSink(RedisSinkProperty redisSinkProperty) {
        this.redisSinkProperty = redisSinkProperty;
    }

    @Override
    public ChangelogMode getChangelogMode(ChangelogMode requestedMode) {
        return ChangelogMode.newBuilder()
                .addContainedKind(RowKind.INSERT)
                .addContainedKind(RowKind.DELETE)
                .addContainedKind(RowKind.UPDATE_BEFORE)
                .addContainedKind(RowKind.UPDATE_AFTER)
                .build();
    }

    @Override
    public SinkRuntimeProvider getSinkRuntimeProvider(Context context) {

        FlinkJedisPoolConfig conf = new FlinkJedisPoolConfig.Builder()
                .setHost(redisSinkProperty.host())
                .setDatabase(redisSinkProperty.database())
                .setPort(redisSinkProperty.port())
                .setPassword(redisSinkProperty.password())
                .setMaxTotal(72)
                .setMinIdle(8)
                .setMaxIdle(72)
                .setTimeout(6000)
                .build();

        if (redisSinkProperty.dataType().trim().equals("hash")) {
            RedisSinkMapperHash mapper = new RedisSinkMapperHash(redisSinkProperty);
            RedisProducer producer = new RedisProducer(conf, mapper);
            return SinkFunctionProvider.of(producer);
        } else if (redisSinkProperty.dataType().trim().equals("hash-increase")) {
            RedisSinkMapperHashIncrease mapper = new RedisSinkMapperHashIncrease(redisSinkProperty);
            RedisProducer producer = new RedisProducer(conf, mapper);
            return SinkFunctionProvider.of(producer);
        } else if (redisSinkProperty.dataType().trim().equals("zset")) {
            RedisSinkMapperZSET mapper = new RedisSinkMapperZSET(redisSinkProperty);
            RedisProducer producer = new RedisProducer(conf, mapper);
            return SinkFunctionProvider.of(producer);
        } else {
            RedisSinkMapper mapper = new RedisSinkMapper(redisSinkProperty);
            RedisProducer producer = new RedisProducer(conf, mapper);
            return SinkFunctionProvider.of(producer);
        }
    }

    @Override
    public DynamicTableSink copy() {
        return new RedisDynamicTableSink(redisSinkProperty);
    }

    @Override
    public String asSummaryString() {
        return "hipac-redis-sink-table";
    }
}
