package com.demo.options;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

/**
 * @fileName: RequestParams.java
 * @description: RequestParams.java类说明
 * @author: by echo huang
 * @date: 2021/1/17 6:33 下午
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class RequestParamOptions implements Serializable {

    private static final long serialVersionUID = 8400446324140800001L;
    private String requestUrl;
    private String formatClassName;
    private String headers;
    private String requestType;

    public static enum RequestType {
        GET, POST, PUT, DELETE, PATCH;
    }
}
