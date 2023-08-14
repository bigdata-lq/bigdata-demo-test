package com.demo.connector.redis;

import com.yangt.redis.config.FlinkJedisConfigBase;
import com.yangt.redis.container.RedisCommandsContainer;
import com.yangt.redis.container.RedisCommandsContainerBuilder;
import com.yangt.redis.mapper.RedisAdditionalMapper;
import com.yangt.redis.mapper.RedisCommand;
import com.yangt.redis.mapper.RedisCommandDescription;
import com.yangt.redis.mapper.RedisMapper;
import com.yangt.util.FastJsonUtil;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.sink.RichSinkFunction;
import org.apache.flink.table.data.RowData;
import org.apache.flink.types.RowKind;
import org.apache.flink.util.Preconditions;


public class RedisProducer extends RichSinkFunction<RowData> {
    private String additionalKey;
    private RedisMapper<RowData> redisSinkMapper;
    private RedisCommand redisCommand;

    private FlinkJedisConfigBase flinkJedisConfigBase;
    private RedisCommandsContainer redisCommandsContainer;

    public RedisProducer(FlinkJedisConfigBase flinkJedisConfigBase, RedisMapper<RowData> redisSinkMapper) {
        Preconditions.checkNotNull(flinkJedisConfigBase, "Redis connection pool config should not be null");
        Preconditions.checkNotNull(redisSinkMapper, "Redis Mapper can not be null");
        Preconditions.checkNotNull(redisSinkMapper.getCommandDescription(), "Redis Mapper data type description can not be null");

        this.flinkJedisConfigBase = flinkJedisConfigBase;

        this.redisSinkMapper = redisSinkMapper;
        RedisCommandDescription redisCommandDescription = redisSinkMapper.getCommandDescription();
        this.redisCommand = redisCommandDescription.getCommand();
        this.additionalKey = redisCommandDescription.getAdditionalKey();
    }

    @Override
    public void open(Configuration parameters) throws Exception {
        super.open(parameters);
        this.redisCommandsContainer = RedisCommandsContainerBuilder.build(this.flinkJedisConfigBase);

    }

    @Override
    public void invoke(RowData input, Context context) throws Exception {
        // 判断是否要处理fase的情况
        RowKind rowKind = input.getRowKind();
        if (rowKind == RowKind.UPDATE_BEFORE) {
            return;
        }


        String key = redisSinkMapper.getKeyFromData(input);
        String value = redisSinkMapper.getValueFromData(input);
        Integer expireTime = redisSinkMapper.getExpireTime(input);

        // 内部的key,只有hash,zset等类型才有
        String internalKey = "";

        if (redisSinkMapper instanceof RedisAdditionalMapper) {
            RedisAdditionalMapper redisAdditionalMapper = (RedisAdditionalMapper) this.redisSinkMapper;
            internalKey = redisAdditionalMapper.getAdditionalKey(input);
        }

        if (!redisSinkMapper.isNotDelAdditionalKey(input)) {
            switch (redisCommand) {
                case SET:
                    this.redisCommandsContainer.delete(key);
                    break;
                case SADD:
                    this.redisCommandsContainer.srem(key, value);
                    break;
                case HSET:
                    this.redisCommandsContainer.hdel(key, internalKey);
                    break;
                case ZADD:
                    this.redisCommandsContainer.zrem(key, value);
                    break;
                default:
                    break;
            }
        } else {
            // 忽略删除删除回撤的情况
            if (rowKind == RowKind.DELETE) {
                return;
            }
            switch (redisCommand) {
                case RPUSH:
                    this.redisCommandsContainer.rpush(key, value);
                    break;
                case LPUSH:
                    this.redisCommandsContainer.lpush(key, value);
                    break;
                case SADD:
                    this.redisCommandsContainer.sadd(key, value);
                    break;
                case SET:
                    this.redisCommandsContainer.set(key, value);
                    break;
                case PFADD:
                    this.redisCommandsContainer.pfadd(key, value);
                    break;
                case PUBLISH:
                    this.redisCommandsContainer.publish(key, value);
                    break;
                case ZADD:
                    this.redisCommandsContainer.zadd(key, internalKey, value);
                    break;
                case HSET:
                    this.redisCommandsContainer.hset(key, internalKey, value);
                    break;
                case HINCRBY:
                    this.redisCommandsContainer.hincrBy(key, internalKey, Long.parseLong(value));
                    break;
                case HMSET:
                    this.redisCommandsContainer.hmset(key, FastJsonUtil.string2Map(value));
                    break;
                default:
                    throw new IllegalArgumentException("Cannot process such data type: " + redisCommand);
            }
        }

        if (expireTime != null) {
            this.redisCommandsContainer.expire(key, expireTime);
        }


    }

    @Override
    public void close() throws Exception {
        if (redisCommandsContainer != null) {
            redisCommandsContainer.close();
        }
        super.close();
    }
}
