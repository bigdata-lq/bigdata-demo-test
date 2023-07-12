package com.demo.udxf;

import com.alibaba.fastjson.JSON;
import org.apache.flink.table.functions.ScalarFunction;

/**
 * 判断json内部,jsonKey对应的value是否为true, 其他情况为false
 */
public class ParseBooleanJsonUDF extends ScalarFunction {
    public Boolean eval(String json, String jsonKey) {

        if (json == null || json.length() == 0 || json.equals("(null)")) {
            return false;
        }


        Boolean res = JSON.parseObject(json).getBoolean(jsonKey);
        if (res == null) {
            return false;
        }

        return res;
    }
}
