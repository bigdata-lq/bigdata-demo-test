import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.util.Properties;

public class KafkaProducerTest {

    KafkaProducer<String, String> producer = null;

    @Before
    public void before()  {
        final Properties kafkaProps = new Properties();
        kafkaProps.put("bootstrap.servers", "test-kafka1-idc.yangtuojia.com:9092,test-kafka2-idc.yangtuojia.com:9092");
        kafkaProps.put("acks", "all");
        kafkaProps.put("retries", 0);
        kafkaProps.put("batch.size", 16384);
        kafkaProps.put("linger.ms", 1);
        kafkaProps.put("buffer.memory", 33554432);
        kafkaProps.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        kafkaProps.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        producer = new KafkaProducer<>(kafkaProps);
    }

    @Test
    public void test() throws Exception {
        String key = "";
        String value = "{\"ts\": 1588232299070, \"id\": 7, \"name\":\"lq2\"}";
        RecordMetadata rm = producer.send(new ProducerRecord<>("hbtest4",
                value)
        ).get();
        System.out.println("Topic " + rm.partition() + " offset " + rm.offset());
    }

    @After
    public void after()  {
        producer.close();
    }
}
