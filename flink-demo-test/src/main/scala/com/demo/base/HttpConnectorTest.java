package com.demo.base;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.EnvironmentSettings;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;

public class HttpConnectorTest {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        EnvironmentSettings settings = EnvironmentSettings.newInstance()
                .inStreamingMode()
                .useBlinkPlanner()
                .build();
        StreamTableEnvironment tableEnvironment = StreamTableEnvironment.create(env, settings);

        // test custom http
        tableEnvironment.executeSql("create table testhttp(message string,code string,data string)with(" +
                "'http.client.request-url'='https://metaapi.yangtuojia.com/v1/api/queue/get/dw_order_d'," +
                "'connector'='http'," +
                "'format'='json')");


        tableEnvironment.executeSql("CREATE TABLE print_table WITH ('connector' = 'print') LIKE testhttp (EXCLUDING ALL)");

        tableEnvironment.executeSql("insert into print_table select * from testhttp").print();
        env.execute("the http connector demo ");
    }
}
