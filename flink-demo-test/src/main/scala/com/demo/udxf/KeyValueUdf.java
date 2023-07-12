package com.demo.udxf;


import com.demo.utils.AttributeUtils;
import org.apache.commons.lang3.StringUtils;
import org.apache.flink.table.functions.ScalarFunction;

import java.util.Map;

public class KeyValueUdf extends ScalarFunction {

    public String eval(String key, String attribute) throws Exception {
        if (StringUtils.isEmpty(attribute)) {
            return "";
        }
        Map<String, String> map = AttributeUtils.attributesToMap(attribute);
        if (map.containsKey(key)) {

            return map.get(key);
        }

        return "";
    }

}


