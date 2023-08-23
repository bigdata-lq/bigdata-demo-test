package com.demo.connector.kafka;

import com.google.common.collect.Sets;
import org.apache.flink.api.common.serialization.DeserializationSchema;
import org.apache.flink.configuration.ConfigOption;
import org.apache.flink.configuration.ConfigOptions;
import org.apache.flink.configuration.ReadableConfig;
import org.apache.flink.table.connector.format.DecodingFormat;
import org.apache.flink.table.connector.source.DynamicTableSource;
import org.apache.flink.table.data.RowData;
import org.apache.flink.table.factories.DeserializationFormatFactory;
import org.apache.flink.table.factories.DynamicTableSourceFactory;
import org.apache.flink.table.factories.FactoryUtil;

import java.util.Set;


public class MetricsKafkaDynamicTableFactory implements DynamicTableSourceFactory {

    public static final String CUSTOMER_IDENTIFIER = "metrics_kafka";
    public static final ConfigOption<String> key_topic = ConfigOptions.key("topic").stringType().noDefaultValue();
    public static final ConfigOption<String> key_bootstrapServers = ConfigOptions.key("properties.bootstrap.servers").stringType().noDefaultValue();
    public static final ConfigOption<String> key_groupId = ConfigOptions.key("properties.group.id").stringType().noDefaultValue();
    public static final ConfigOption<String> key_format = ConfigOptions.key("format").stringType().defaultValue("json");


    @Override
    public DynamicTableSource createDynamicTableSource(Context context) {
        FactoryUtil.TableFactoryHelper helper = FactoryUtil.createTableFactoryHelper(this, context);
        // 发现实现的DeserializationFormatFactory 获取反序列化工厂
        DecodingFormat<DeserializationSchema<RowData>> decodingFormat =
                helper.discoverDecodingFormat(DeserializationFormatFactory.class, FactoryUtil.FORMAT);
        // 校验table参数
        helper.validate();
        ReadableConfig options = helper.getOptions();
        String topic = options.get(key_topic);
        String bootstrapServers = options.get(key_bootstrapServers);
        String groupId = options.get(key_groupId);
        return new MetricsKafkaTableSource(decodingFormat, topic, bootstrapServers, groupId);
    }

    @Override
    public String factoryIdentifier() {
        return CUSTOMER_IDENTIFIER;
    }

    @Override
    public Set<ConfigOption<?>> requiredOptions() {
        return Sets.newHashSet(key_topic, key_bootstrapServers, key_format);
    }

    @Override
    public Set<ConfigOption<?>> optionalOptions() {
        return Sets.newHashSet(key_groupId);
    }
}
