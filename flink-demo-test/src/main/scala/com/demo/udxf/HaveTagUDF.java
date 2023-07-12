package com.demo.udxf;

import org.apache.commons.collections.CollectionUtils;
import org.apache.commons.lang3.StringUtils;
import org.apache.flink.table.functions.ScalarFunction;

import java.util.Arrays;
import java.util.List;

public class HaveTagUDF extends ScalarFunction {
    public Boolean eval(String key, String tags) {
        if (StringUtils.isEmpty(tags) || StringUtils.isEmpty(key)) {
            return false;
        }
        String[] tagsArray = StringUtils.split(tags, ",");

        List<String> arrayList = Arrays.asList(tagsArray);
        if (CollectionUtils.isEmpty(arrayList)) {
            return false;
        }
        if (arrayList.contains(key)) {
            return true;
        }
        return false;
    }
}
