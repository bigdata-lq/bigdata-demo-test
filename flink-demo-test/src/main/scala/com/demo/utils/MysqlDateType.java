package com.demo.utils;

import org.apache.commons.lang3.StringUtils;

/**
 * @description:
 * @author: liquan
 * @time: 2020/8/12 0012 下午 15:31
 */
public enum MysqlDateType {

    TINYINT,SMALLINT,MEDIUMINT,INT,INTEGER,BIGINT,FLOAT,DOUBLE,DECIMAL;

    MysqlDateType() {
    }

    public static Boolean isNumberType(String typeName){
        if(StringUtils.isBlank(typeName)){
            return false;
        }
        for (MysqlDateType mysqlDateType: MysqlDateType.values()){
            if(mysqlDateType.name().toLowerCase().equals(typeName)){
                return true;
            }
        }
        return false;
    }
}
