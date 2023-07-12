package com.demo.connector.http;

import com.demo.options.ConnectionOptions;
import com.demo.options.HttpClientOptions;
import com.demo.options.RequestParamOptions;
import com.demo.utils.OkHttpClientUtils;
import com.google.common.base.Preconditions;
import okhttp3.*;
import org.apache.commons.lang3.ArrayUtils;
import org.apache.flink.api.common.serialization.DeserializationSchema;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.api.java.typeutils.ResultTypeQueryable;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.source.RichSourceFunction;
import org.apache.flink.table.data.RowData;

import java.io.IOException;
import java.util.Objects;

public class HttpSourceFunction extends RichSourceFunction<RowData> implements ResultTypeQueryable<RowData> {

    private final RequestParamOptions requestParamOptions;
    private final ConnectionOptions connectionOptions;
    private final HttpClientOptions httpClientOptions;
    private final DeserializationSchema<RowData> deserializer;
    private transient OkHttpClient httpClient;
    private boolean isRunning = true;

    public HttpSourceFunction(RequestParamOptions requestParamOptions, ConnectionOptions connectionOptions, HttpClientOptions httpClientOptions, DeserializationSchema<RowData> deserializer) {
        this.requestParamOptions = requestParamOptions;
        this.connectionOptions = connectionOptions;
        this.httpClientOptions = httpClientOptions;
        this.deserializer = deserializer;
    }

    @Override
    public void open(Configuration parameters) throws Exception {
        OkHttpClientUtils okHttpClientUtils = new OkHttpClientUtils();
        this.httpClient = okHttpClientUtils.initialHttpClient(httpClientOptions, connectionOptions, false);
    }

    @Override
    public TypeInformation<RowData> getProducedType() {
        return deserializer.getProducedType();
    }

    @Override
    public void run(SourceContext<RowData> ctx) throws Exception {
        while (isRunning) {
            String headers = requestParamOptions.getHeaders();
            String requestType = requestParamOptions.getRequestType();
            String[] headersArr = headers.split(",");
            Call request = null;
            if (ArrayUtils.isNotEmpty(headersArr)) {
                for (String headerKv : headersArr) {
                    String[] headerKvArr = headerKv.split(":");
//                    Preconditions.checkArgument(ArrayUtils.isNotEmpty(headerKvArr) && headerKv.length() == 2, "header参数异常");

                    switch (RequestParamOptions.RequestType.valueOf(requestType)) {
                        case GET:
                            request = httpClient.newCall(new Request.Builder().get().url(requestParamOptions.getRequestUrl()).build());
                            break;
                        case PATCH:
                            break;
                        case POST:
                            break;
                        case DELETE:
                            break;
                        default:
                            throw new RuntimeException("请求类型不支持");
                    }
                }
                if (null != request) {
                    //异步调用
                    request.enqueue(new Callback() {
                        @Override
                        public void onFailure(Call call, IOException e) {

                        }

                        @Override
                        public void onResponse(Call call, Response response) throws IOException {
                            ResponseBody body = response.body();
                            String data = body.string();
//                            System.out.println("onResponse: " + data);
                            ctx.collect(deserializer.deserialize(data.getBytes()));
                        }
                    });
//                    ResponseBody body = request.execute().body();
//                    byte[] result = Objects.requireNonNull(request.execute().body()).bytes();

                }
            }
        }
    }

    @Override
    public void cancel() {
        isRunning = false;
        httpClient = null;
    }
}
