package com.demo.connector.kafka;

import org.apache.flink.api.common.functions.RuntimeContext;
import org.apache.flink.metrics.Counter;
import org.apache.flink.metrics.Gauge;
import org.apache.flink.shaded.jackson2.com.fasterxml.jackson.databind.JsonNode;
import org.apache.flink.shaded.jackson2.com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.flink.shaded.jackson2.com.fasterxml.jackson.databind.node.ObjectNode;
import org.apache.flink.streaming.connectors.kafka.internals.AbstractFetcher;
import org.apache.flink.streaming.connectors.kafka.internals.KafkaConsumerThread;
import org.apache.flink.streaming.connectors.kafka.internals.KafkaFetcher;
import org.apache.flink.streaming.util.serialization.JSONKeyValueDeserializationSchema;
import org.apache.flink.types.Row;
import org.apache.flink.util.Collector;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.consumer.internals.SubscriptionState;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.common.internals.PartitionStates;

import java.lang.reflect.Field;
import java.util.Set;

/**
 * 自定义json序列化对象
 *
 */
public class MetricsJsonDeserialization extends JSONKeyValueDeserializationSchema {

    private String DT_TOPIC_GROUP = "topic";
    private String DT_PARTITION_GROUP = "partition";
    private String DT_TOPIC_PARTITION_LAG_GAUGE = "topic_partition_lag";
    private Counter inCounter;
    private Counter outCounter;
    boolean firstMsg = true;

    private AbstractFetcher<Row, ?> fetcher;
    private ObjectMapper mapper;

    private final boolean includeMetadata;
    private RuntimeContext runtimeContext;



    public MetricsJsonDeserialization(boolean includeMetadata) {
        super(includeMetadata);
        this.includeMetadata = includeMetadata;
    }

    public void initMetric(){
        this.inCounter =
                runtimeContext.getMetricGroup()
                        .addGroup("web-streaming")
                        .counter("in-count");

        this.outCounter =
                runtimeContext.getMetricGroup().addGroup("web-streaming").counter("out-count");

    }

    public void setFetcher(AbstractFetcher<Row, ?> fetcher) {
        this.fetcher = fetcher;
    }

    public void setRuntimeContext(RuntimeContext runtimeContext){
        this.runtimeContext = runtimeContext;
    }

    @Override
    public void deserialize(ConsumerRecord<byte[], byte[]> record, Collector<ObjectNode> out) throws Exception {
        inCounter.inc();

        if(firstMsg){
            // 只有在第一条数据到来的时候，才会调用该方法
            registerPtMetric(fetcher);
            firstMsg = false;
        }
        if (mapper == null) {
            mapper = new ObjectMapper();
        }
        ObjectNode node = mapper.createObjectNode();
        if (record.key() != null) {
            node.set("key", mapper.readValue(record.key(), JsonNode.class));
        }
        if (record.value() != null) {
            node.set("value", mapper.readValue(record.value(), JsonNode.class));
        }
        if (includeMetadata) {
            node.putObject("metadata")
                    .put("offset", record.offset())
                    .put("topic", record.topic())
                    .put("partition", record.partition());
        }
        outCounter.inc();
        out.collect(node);
    }

    protected void registerPtMetric(AbstractFetcher<Row, ?> fetcher) throws Exception {
        // 通过反射获取fetcher中的kafka消费者等信息, 反射获取属性路径如下：
        // Flink: Fetcher -> KafkaConsumerThread -> KafkaConsumer ->
        // Kafka Consumer: KafkaConsumer -> SubscriptionState -> partitionLag()
        Field consumerThreadField = ((KafkaFetcher) fetcher).getClass().getDeclaredField("consumerThread");

        consumerThreadField.setAccessible(true);
        KafkaConsumerThread consumerThread = (KafkaConsumerThread) consumerThreadField.get(fetcher);

        Field hasAssignedPartitionsField = consumerThread.getClass().getDeclaredField("hasAssignedPartitions");
        hasAssignedPartitionsField.setAccessible(true);

        boolean hasAssignedPartitions = (boolean) hasAssignedPartitionsField.get(consumerThread);
        if(!hasAssignedPartitions){
            throw new RuntimeException("wait 50 secs, but not assignedPartitions");
        }
        Field consumerField = consumerThread.getClass().getDeclaredField("consumer");
        consumerField.setAccessible(true);
        KafkaConsumer kafkaConsumer = (KafkaConsumer) consumerField.get(consumerThread);
        Field subscriptionStateField = kafkaConsumer.getClass().getDeclaredField("subscriptions");
        subscriptionStateField.setAccessible(true);
        SubscriptionState subscriptionState = (SubscriptionState) subscriptionStateField.get(kafkaConsumer);
        Set<TopicPartition> assignedPartitions = subscriptionState.assignedPartitions();

        Field assignmentField = subscriptionState.getClass().getDeclaredField("assignment");
        assignmentField.setAccessible(true);
        PartitionStates<CustomerTopicPartitionState> assignment = (PartitionStates<CustomerTopicPartitionState>)assignmentField.get(subscriptionState);


        for(TopicPartition topicPartition : assignedPartitions){
            CustomerTopicPartitionState topicPartitionState = assignment.stateValue(topicPartition);
            runtimeContext.getMetricGroup().addGroup(DT_TOPIC_GROUP, topicPartition.topic())
                    .addGroup(DT_PARTITION_GROUP, topicPartition.partition() + "")
                    .gauge(DT_TOPIC_PARTITION_LAG_GAUGE, (Gauge<Long>) () -> topicPartitionState.getLastStableOffset() - topicPartitionState.getPosition());

        }
    }
}
