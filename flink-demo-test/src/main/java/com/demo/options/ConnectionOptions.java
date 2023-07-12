package com.demo.options;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

/**
 * @fileName: ConnectionPoolConfig.java
 * @description: ConnectionPoolConfig.java类说明
 * @author: by echo huang
 * @date: 2021/1/17 5:59 下午
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class ConnectionOptions implements Serializable {
    private static final long serialVersionUID = 1844898349097602559L;
    private int maxIdleConnections;
    private long keepAliveDuration;
    private long connectionTimeout;
}
