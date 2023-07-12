package com.demo.udxf.model;

public class Promotion {
    private String bizId;

    private Integer bizType;

    private Long bizAmount;

    public Promotion() {
    }

    public String getBizId() {
        return bizId;
    }

    public void setBizId(String bizId) {
        this.bizId = bizId;
    }

    public Integer getBizType() {
        return bizType;
    }

    public void setBizType(Integer bizType) {
        this.bizType = bizType;
    }

    public Long getBizAmount() {
        return bizAmount;
    }

    public void setBizAmount(Long bizAmount) {
        this.bizAmount = bizAmount;
    }

}
