package com.struct.linked;

/**
 * @description: 单链表
 * @author: liquan
 * @time: 2022/11/16 0016 下午 17:44
 */
public class OneListNode {
    /**
     * 值
     */
    int val ;

    /**
     * 虚拟节点
     */
    OneListNode next;

    OneListNode(){}

    OneListNode(int val) {
        this.val=val;
    }

}
