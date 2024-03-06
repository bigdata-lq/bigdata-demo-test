package com.udf.udf;

import org.apache.hadoop.hive.ql.exec.UDF;

public class ToLowerCase extends UDF {
    // 必须是 public，并且 evaluate 方法可以重载
    public String evaluate(String field) {
        String result = field.toLowerCase();
        return result;
    }
}
