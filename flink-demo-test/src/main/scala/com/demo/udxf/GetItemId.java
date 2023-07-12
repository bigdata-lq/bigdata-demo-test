package com.demo.udxf;

import com.alibaba.fastjson.JSON;
import org.apache.flink.table.functions.ScalarFunction;

/**
 * 给RecoStreamingJob用的特定的udf函数
 */
public class GetItemId extends ScalarFunction {
    public String eval(String json) {

        String itemId = null;

        try {
            if (json == null || json.length() == 0 || json.equals("(null)")) {
                return null;
            } else if (json.contains("itemId")) {
                itemId = JSON.parseObject(json).get("itemId").toString();
            } else if (json.contains("item_id")) {
                itemId = JSON.parseObject(json).get("item_id").toString();
            } else {
                return null;
            }
        } catch (Exception e) {
            // 脏数据过滤掉,返回null
            itemId = null;
        }

        if (itemId != null && itemId.contains(",")) {
            return null;
        }
        return itemId;
    }


    public static void main(String[] args) {
        String str1 = "{\"itemId\":\"13108\"}";
        String str2 = "{\"item_id\":168646,\"resource_type\":0,\"source_type\":3,\"model_id\":901,\"search_result_items_type\":0,\"search_type\":\"1589950221145_0\",\"search_id\":\"1589950221145\",\"is_coupon\":0,\"sort_type\":3,\"flow_item_flag\":false,\"price\":\"261.00-278.83\",\"item_source_type\":0,\"position\":3,\"stock\":3414,\"source_child_type\":32,\"search_time\":1589950221145,\"search_text\":\" 启赋4\"}";
        System.out.println(new GetItemId().eval(str1));
        System.out.println(new GetItemId().eval(str2));

    }

}
