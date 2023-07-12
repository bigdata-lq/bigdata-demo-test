package com.demo.udxf;

import com.alibaba.fastjson.JSON;
import org.apache.flink.table.functions.ScalarFunction;

public class ParseJsonUDF extends ScalarFunction {
    public String eval(String json, String jsonKey) {
        String res = JSON.parseObject(json).getString(jsonKey);
        return res;
    }
}
