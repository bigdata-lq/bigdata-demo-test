package com.demo.udxf;

import org.apache.commons.lang3.StringUtils;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.api.common.typeinfo.Types;
import org.apache.flink.api.java.typeutils.RowTypeInfo;
import org.apache.flink.table.functions.TableFunction;
import org.apache.flink.types.Row;

/**
 * @description:
 * @author: liquan
 * @time: 2020/6/3 0003 下午 15:03
 */
public class StringTwoSplitUDTF extends TableFunction<Row> {

    public void eval(String value, String separator1, String separator2) {
        if(StringUtils.isEmpty(value)){
            return;
        }
        String[] rows = value.split(separator1);
        for(int i = 0; i < rows.length; i++){
            String[] fields = rows[i].split(separator2);
            Row row = new Row(2);
            row.setField(0, fields[0]);
            if(fields.length == 2) {
                row.setField(1, fields[1]);
            } else {
                row.setField(1, "");
            }
            collect(row);
        }
    }

    @Override
    public TypeInformation<Row> getResultType() {
        return new RowTypeInfo(Types.STRING, Types.STRING);
    }

}
