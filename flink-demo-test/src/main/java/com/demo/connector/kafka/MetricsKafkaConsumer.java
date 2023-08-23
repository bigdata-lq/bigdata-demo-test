package com.demo.connector.kafka;

import org.apache.flink.api.common.serialization.DeserializationSchema;
import org.apache.flink.metrics.MetricGroup;
import org.apache.flink.streaming.api.operators.StreamingRuntimeContext;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;
import org.apache.flink.streaming.connectors.kafka.KafkaDeserializationSchema;
import org.apache.flink.streaming.connectors.kafka.config.OffsetCommitMode;
import org.apache.flink.streaming.connectors.kafka.internals.AbstractFetcher;
import org.apache.flink.util.SerializedValue;

import java.util.List;
import java.util.Map;
import java.util.Properties;

/**
 * 自定义kafka连接器,支持上报topic partition 消费延迟指标 pushgateway + prometheus
 */
public class MetricsKafkaConsumer extends FlinkKafkaConsumer {

    private static final long serialVersionUID = -1234567890L;
    private MetricsJsonDeserialization customerJsonDeserialization;


    public MetricsKafkaConsumer(List topics, KafkaDeserializationSchema deserializer, Properties props) {
        super(topics, deserializer, props);
        this.customerJsonDeserialization = (MetricsJsonDeserialization) deserializer;
    }

    @Override
    public void run(SourceContext sourceContext) throws Exception {
        //反序列化时 初始化消费延迟指标metrics
        customerJsonDeserialization.setRuntimeContext(getRuntimeContext());
        customerJsonDeserialization.initMetric();
        super.run(sourceContext);
    }

    @Override
    protected AbstractFetcher createFetcher(SourceContext sourceContext, Map assignedPartitionsWithInitialOffsets, SerializedValue watermarkStrategy, StreamingRuntimeContext runtimeContext, OffsetCommitMode offsetCommitMode, MetricGroup consumerMetricGroup, boolean useMetrics) throws Exception {
        AbstractFetcher fetcher = super.createFetcher(sourceContext, assignedPartitionsWithInitialOffsets, watermarkStrategy, runtimeContext, offsetCommitMode, consumerMetricGroup, useMetrics);
        customerJsonDeserialization.setFetcher(fetcher);
        return fetcher;
    }
}
