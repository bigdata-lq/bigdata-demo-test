package com.demo.format;

import com.alibaba.fastjson.JSONObject;
import com.demo.utils.MysqlDateType;
//import com.yangt.model.canal.DataMessage;
//import com.yangt.model.canal.Field;
import org.apache.commons.collections.CollectionUtils;
import org.apache.commons.lang3.StringUtils;
import org.apache.flink.api.common.serialization.DeserializationSchema;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.table.connector.source.DynamicTableSource;
import org.apache.flink.table.data.RowData;
import org.apache.flink.table.types.logical.LogicalTypeRoot;
import org.apache.flink.table.types.logical.RowType;
import org.apache.flink.types.Row;
import org.apache.flink.types.RowKind;
import org.apache.flink.util.Collector;

import java.io.IOException;
import java.util.List;

public class CDCJsonDeserializationSchema implements DeserializationSchema<RowData> {

    private static final long serialVersionUID = 1L;
    private final TypeInformation<RowData> resultTypeInfo;
    private final RowType rowType ;
    private final DynamicTableSource.DataStructureConverter dataStructureConverter;
//    private final JsonRowDataDeserializationSchema jsonDeserializer;


    public CDCJsonDeserializationSchema(RowType rowType , TypeInformation<RowData> resultTypeInfo,
                                        DynamicTableSource.DataStructureConverter dataStructureConverter) {
        this.resultTypeInfo = resultTypeInfo;
        this.rowType = rowType;
        this.dataStructureConverter = dataStructureConverter;
        // 序列化json
//        this.jsonDeserializer = new JsonRowDataDeserializationSchema(this.createJsonRowType(), resultTypeInfo,
//                JsonOptions.FAIL_ON_MISSING_FIELD, JsonOptions.IGNORE_PARSE_ERRORS, JsonOptions.TIMESTAMP_FORMAT);
    }

    @Override
    public RowData deserialize(byte[] bytes) throws IOException {
        throw new RuntimeException("Please invoke DeserializationSchema#deserialize(byte[], Collector<RowData>) instead.");
    }

    @Override
    public void deserialize(byte[] message, Collector<RowData> out) throws IOException {
//        DataMessage dataMessage = JSONObject.parseObject(new String(message), DataMessage.class);
//        JSONObject jsonObject = changeDataMessage(dataMessage);
        JSONObject jsonObject = new JSONObject();
        Row row = new Row(RowKind.INSERT, rowType.getFieldCount());
//        GenericRowData insert = new GenericRowData(rowType.getFieldCount());
//        for(String fieldName : rowType.getFieldNames()){
//            int fieldIndex = rowType.getFieldIndex(fieldName);
//            Object value = jsonObject.get(fieldName);
//            insert.setField(fieldIndex,value);
//        }
//        insert.setRowKind(RowKind.INSERT); //TD
        List<RowType.RowField> fields = rowType.getFields();
        for(int i = 1; i < rowType.getFieldCount(); i++){
            RowType.RowField rowField = fields.get(i);
            LogicalTypeRoot typeRoot = rowField.getType().getTypeRoot();
            String name = rowField.getName();
            String value = jsonObject.getString(name);
            row.setField(i, parse(typeRoot,value));
        }
        out.collect((RowData) dataStructureConverter.toInternal(row));
    }

    @Override
    public boolean isEndOfStream(RowData rowData) {
        return false;
    }

    @Override
    public TypeInformation<RowData> getProducedType() {
        return this.resultTypeInfo;
    }

//    private static JSONObject changeDataMessage(DataMessage dataMessage){
//        JSONObject jsonObject = new JSONObject();
//        jsonObject.put("_execute_time", dataMessage.getExecuteTime());
//        jsonObject.put("_table_name", dataMessage.getTableName());
//        jsonObject.put("_db_name", dataMessage.getDbName());
//        jsonObject.put("_op_type", dataMessage.getOpType());
//        jsonObject.put("_change_column", list2JsonString(dataMessage.getChangeColumn()));
//        jsonObject.put("_old_column", list2JsonString(dataMessage.getOldColumn()));
//        jsonObject.put("_ddl_field", list2JsonString(dataMessage.getDdlField()));
//        for (Field field : dataMessage.getNewColumn()) {
//            if(MysqlDateType.isNumberType(field.getType().toLowerCase()) && field.isValueNull()){
//                jsonObject.put(field.getFieldName(), null);
//            } else {
//                jsonObject.put(field.getFieldName(), field.getValue());
//            }
//        }
//        return jsonObject;
//    }

//    private static String list2JsonString(List<Field> fields){
//        final JSONObject jsonObject = new JSONObject();
//        if(CollectionUtils.isEmpty(fields)){
//            return jsonObject.toString();
//        }
//        for (Field field : fields) {
//            jsonObject.put(field.getFieldName(), field.getValue());
//        }
//        return jsonObject.toString();
//    }

    private static Object parse(LogicalTypeRoot root, String value) {
        if(StringUtils.isBlank(value)){
            return null;
        }
        switch (root) {
            case INTEGER:
                return Integer.parseInt(value);
            case VARCHAR:
                return value;
            case BIGINT:
                return Long.valueOf(value);
            default:
                throw new IllegalArgumentException();
        }
    }
}
