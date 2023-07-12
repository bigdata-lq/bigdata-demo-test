package com.demo.udxf;

import com.alibaba.fastjson.JSON;
import com.demo.udxf.model.Promotion;
import org.apache.commons.collections.CollectionUtils;
import org.apache.commons.lang3.StringUtils;
import org.apache.flink.table.functions.ScalarFunction;

import java.util.List;

public class PromotionAmountUdf extends ScalarFunction {

    public Long eval(Integer bizType, String json) throws Exception {

        if (StringUtils.isEmpty(json) || bizType == null) {
            return 0L;
        }
        List<Promotion> promotionList = JSON.parseArray(json, Promotion.class);
        if (CollectionUtils.isEmpty(promotionList)) {
            return 0L;
        }
        for (Promotion promotion : promotionList) {
            if (bizType.equals(promotion.getBizType())) {
                return promotion.getBizAmount();
            }
        }
        return 0L;
    }

}


