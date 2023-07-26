package com.demo.format;

import org.apache.flink.api.common.serialization.DeserializationSchema;
import org.apache.flink.api.common.serialization.SerializationSchema;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.configuration.ConfigOption;
import org.apache.flink.configuration.ReadableConfig;
import org.apache.flink.formats.common.TimestampFormat;
import org.apache.flink.formats.json.JsonOptions;
import org.apache.flink.formats.json.JsonRowDataSerializationSchema;
import org.apache.flink.table.connector.ChangelogMode;
import org.apache.flink.table.connector.format.DecodingFormat;
import org.apache.flink.table.connector.format.EncodingFormat;
import org.apache.flink.table.connector.sink.DynamicTableSink;
import org.apache.flink.table.connector.source.DynamicTableSource;
import org.apache.flink.table.data.RowData;
import org.apache.flink.table.factories.DeserializationFormatFactory;
import org.apache.flink.table.factories.DynamicTableFactory;
import org.apache.flink.table.factories.FactoryUtil;
import org.apache.flink.table.factories.SerializationFormatFactory;
import org.apache.flink.table.types.DataType;
import org.apache.flink.table.types.logical.RowType;
import org.apache.flink.types.RowKind;

import java.util.Collections;
import java.util.Set;

import static org.apache.flink.formats.json.JsonOptions.MAP_NULL_KEY_LITERAL;

public class YtCDCFormatFactory implements
        DeserializationFormatFactory,
        SerializationFormatFactory {

    /**
     * 反序列化
     * @param context
     * @param readableConfig
     * @return
     */
    @Override
    public DecodingFormat<DeserializationSchema<RowData>> createDecodingFormat(DynamicTableFactory.Context context, ReadableConfig readableConfig) {
        FactoryUtil.validateFactoryOptions(this,readableConfig);
        return new DecodingFormat<DeserializationSchema<RowData>>() {
            @Override
            public ChangelogMode getChangelogMode() {
                return ChangelogMode.insertOnly();
            }

            @Override
            public DeserializationSchema<RowData> createRuntimeDecoder(DynamicTableSource.Context context, DataType dataType) {
                // 表的字段名和数据类型
                RowType rowType = (RowType) dataType.getLogicalType();
                TypeInformation<RowData> rowDataTypeInformation = context.createTypeInformation(dataType);
                DynamicTableSource.DataStructureConverter dataStructureConverter = context.createDataStructureConverter(dataType);
//                LogicalType logicalType = dataType.getLogicalType();
                return new CDCJsonDeserializationSchema(rowType, rowDataTypeInformation, dataStructureConverter);
            }
        };
    }

    /**
     * 序列化  JsonRowDataSerializationSchema
     * @param context
     * @param formatOptions
     * @return
     */
    @Override
    public EncodingFormat<SerializationSchema<RowData>> createEncodingFormat(DynamicTableFactory.Context context, ReadableConfig formatOptions) {
        FactoryUtil.validateFactoryOptions(this, formatOptions);

        TimestampFormat timestampOption = JsonOptions.getTimestampFormat(formatOptions);
        JsonOptions.MapNullKeyMode mapNullKeyMode = JsonOptions.getMapNullKeyMode(formatOptions);
        String mapNullKeyLiteral = formatOptions.get(MAP_NULL_KEY_LITERAL);

        return new EncodingFormat<SerializationSchema<RowData>>() {
            @Override
            public SerializationSchema<RowData> createRuntimeEncoder(
                    DynamicTableSink.Context context,
                    DataType consumedDataType) {
                final RowType rowType = (RowType) consumedDataType.getLogicalType();
                return new JsonRowDataSerializationSchema(rowType, timestampOption, mapNullKeyMode, mapNullKeyLiteral, false);
            }

            @Override
            public ChangelogMode getChangelogMode() {
                return ChangelogMode.newBuilder()
                        .addContainedKind(RowKind.INSERT)
                        .addContainedKind(RowKind.DELETE)
                        .addContainedKind(RowKind.UPDATE_BEFORE)
                        .addContainedKind(RowKind.UPDATE_AFTER)
                        .build();
            }
        };
    }

    @Override
    public String factoryIdentifier() {
        return "yt-cdc";
    }

    @Override
    public Set<ConfigOption<?>> requiredOptions() {
        return Collections.emptySet();
    }

    @Override
    public Set<ConfigOption<?>> optionalOptions() {
        return Collections.emptySet();
    }
}
