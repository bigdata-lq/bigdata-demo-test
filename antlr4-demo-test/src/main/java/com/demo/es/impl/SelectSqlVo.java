package com.demo.es.impl;

import lombok.Data;

import java.util.List;

@Data
public class SelectSqlVo {
    private String startToken;
    private boolean from;
    private List<String> fields;
    private String tableName;

    public boolean isQuery() {
        return "SELECT".equalsIgnoreCase(startToken);
    }


}
