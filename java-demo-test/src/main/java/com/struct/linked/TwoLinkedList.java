package com.struct.linked;

/**
 * @description:
 * @author: liquan
 * @time: 2022/11/16 0016 下午 17:46
 */
public class TwoLinkedList {

    //记录链表中元素的数量
    int size ;

    //记录链表的虚拟头结点和尾结点
    TwoListNode head,tail;

    public TwoLinkedList() {
        this.size = 0 ;
        this.head = new TwoListNode(0);
        this.tail = new TwoListNode(0);
        //这一步非常关键，否则在加入头结点的操作中会出现null.next的错误！！
        head.next = tail;
        tail.next = head;
    }

    public int get(int index) {
        //判断index是否有效
        if(index<0 || index>=size){
            return -1;
        }
        TwoListNode cur = this.head;
        //判断是哪一边遍历时间更短
        if(index >= size / 2){
            //tail开始
            cur = tail;
            for(int i=0; i< size-index; i++){
                cur = cur.prev;
            }
        }else{
            for(int i=0; i<= index; i++){
                cur = cur.next;
            }
        }
        return cur.val;
    }

    public void addAtHead(int val) {
        //等价于在第0个元素前添加
        addAtIndex(0,val);
    }

    public void addAtTail(int val) {
        //等价于在最后一个元素(null)前添加
        addAtIndex(size,val);
    }

    public void addAtIndex(int index, int val) {
        //index大于链表长度
        if(index>size){
            return;
        }
        //index小于0
        if(index<0){
            index = 0;
        }
        size++;
        //找到前驱
        TwoListNode pre = this.head;
        for(int i=0; i<index; i++){
            pre = pre.next;
        }
        //新建结点
        TwoListNode newNode = new TwoListNode(val);
        newNode.next = pre.next;
        pre.next.prev = newNode;
        newNode.prev = pre;
        pre.next = newNode;

    }

    public void deleteAtIndex(int index) {
        //判断索引是否有效
        if(index<0 || index>=size){
            return;
        }
        //删除操作
        size--;
        TwoListNode pre = this.head;
        for(int i=0; i<index; i++){
            pre = pre.next;
        }
        pre.next.next.prev = pre;
        pre.next = pre.next.next;
    }

}
