package com.demo.udxf;

import org.apache.flink.table.functions.ScalarFunction;

public class JsonHasKeyUDF extends ScalarFunction {

    public Boolean eval(String json, String jsonKey) {
        return json.contains(jsonKey);
    }
}
