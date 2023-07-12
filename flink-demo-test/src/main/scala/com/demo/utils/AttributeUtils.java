
package com.demo.utils;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

/**
 * Created by xiaoshuai on 2015/12/10.
 */
public class AttributeUtils {

    /**
     * attributes字段中的属性之间的分隔符
     */
    private static final String SEMICOLON = ";";

    /**
     * attributes字段中属性key和value之间的分隔符
     */
    private static final String COLON     = ":";

    /**
     * 将attributes中的字符串转换成map,key1:v1;key2:v2
     * 
     * @param attributes
     * @return
     */
    public static Map<String, String> attributesToMap(String attributes) {
        if ((attributes == null) || ("".equals(attributes))) {
            return new HashMap<String, String>();
        }

        Map<String, String> map = new HashMap<String, String>();

        // 获取所有属性数组
        String[] attrs = attributes.split(SEMICOLON);
        if ((attrs != null) && (attrs.length > 0)) {
            for (String attr : attrs) {
                // 获取key和value
                String[] keyValue = attr.split(COLON);
                if ((keyValue != null) && (keyValue.length > 1) && keyValue[0] != null) {
                    map.put(keyValue[0], keyValue[1]);
                }
            }
        }
        return map;

    }

    /**
     * @param map map
     * @return 字符串
     * @description 将map转换成字符串
     */
    public static String getStringAttributes(Map<String, String> map) {
        if ((map == null) || (map.size() == 0)) {
            return "";
        }
        StringBuilder sb = new StringBuilder();
        Set<Map.Entry<String, String>> entrySet = map.entrySet();
        for (Map.Entry<String, String> entry : entrySet) {
            sb.append(entry.getKey());
            sb.append(COLON);
            sb.append(entry.getValue());
            sb.append(SEMICOLON);
        }
        return sb.toString();
    }

    /**
     * @return 字符串
     * @description 将attributes中的字符中对应的key的value更新
     */
    public static String updateAttributes(String attributes, String key, String value) {
        Map<String, String> map = attributesToMap(attributes);
        map.put(key, value);

        return getStringAttributes(map);
    }

    /**
     * @param attributes 源属性字符串
     * @param key 待查询的对应属性
     * @description 如key1:v1;key2:v2。查key1返回v1
     */
    public static String getAttributesByKey(String attributes, String key) {
        Map<String, String> map = AttributeUtils.attributesToMap(attributes);

        String value = map.get(key);
        if (value == null) {
            return "";
        }
        return value.trim();
    }
}
