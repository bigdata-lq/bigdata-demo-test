package com.demo.options;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

/**
 * @fileName: HttpClientConfig.java
 * @description: HttpClientConfig.java类说明
 * @author: by echo huang
 * @date: 2021/1/17 5:59 下午
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class HttpClientOptions implements Serializable {
    private static final long serialVersionUID = 8252040654170490539L;
    private Long heartInterval;
    private Long readTimeout ;
    private Long writeTimeout;
}
