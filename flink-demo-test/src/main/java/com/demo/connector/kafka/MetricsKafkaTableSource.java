package com.demo.connector.kafka;


import com.google.common.collect.Lists;
import org.apache.flink.api.common.serialization.DeserializationSchema;
import org.apache.flink.configuration.ConfigOption;
import org.apache.flink.configuration.ConfigOptions;
import org.apache.flink.table.connector.ChangelogMode;
import org.apache.flink.table.connector.format.DecodingFormat;
import org.apache.flink.table.connector.source.DynamicTableSource;
import org.apache.flink.table.connector.source.ScanTableSource;
import org.apache.flink.table.connector.source.SourceFunctionProvider;
import org.apache.flink.table.data.RowData;

import java.util.Properties;

public class MetricsKafkaTableSource implements ScanTableSource {

    private final DecodingFormat<DeserializationSchema<RowData>> decodingFormat;
    private final String topic ;
    private final String bootstrapServers ;
    private final String groupId ;

    public MetricsKafkaTableSource(DecodingFormat<DeserializationSchema<RowData>> decodingFormat, String topic, String bootstrapServers, String groupId) {
        this.decodingFormat = decodingFormat;
        this.topic = topic;
        this.bootstrapServers = bootstrapServers;
        this.groupId = groupId;
    }

    @Override
    public ChangelogMode getChangelogMode() {
        return decodingFormat.getChangelogMode();
    }

    @Override
    public ScanRuntimeProvider getScanRuntimeProvider(ScanContext runtimeProviderContext) {
        Properties properties = new Properties();
        properties.setProperty("bootstrap.servers", bootstrapServers);
        //重写序列化json
        MetricsKafkaConsumer metricsKafkaConsumer = new MetricsKafkaConsumer(Lists.newArrayList(topic), new MetricsJsonDeserialization(true), properties);
        return SourceFunctionProvider.of(metricsKafkaConsumer, false);
    }

    @Override
    public DynamicTableSource copy() {
        return null;
    }

    @Override
    public String asSummaryString() {
        return null;
    }
}
