package com.demo.udxf;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import org.apache.commons.lang3.StringUtils;
import org.apache.flink.table.functions.ScalarFunction;

/**
 * @description: 根据json中的key获取value
 * @author: liquan
 * @time: 2020/6/4 0004 上午 9:50
 */
public class jsonTupleUDF extends ScalarFunction {

    public String eval(String json, String fieldName) {
        if(StringUtils.isBlank(json)|| StringUtils.isBlank(json)){
            return null;
        }
        JSONObject jsonObject = JSON.parseObject(json);
        Object fieldValue = jsonObject.get(fieldName);
        if(fieldValue == null){
            return null;
        }
        return fieldValue.toString();
    }

}

