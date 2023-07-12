package com.struct.current;

import java.util.LinkedList;
import java.util.Queue;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class ConditionTest {

    public static void main(String[] args) {
        Queue<String> queue = new LinkedList<>();
        // 重入锁
        Lock lock = new ReentrantLock();
        // 通过Lock.newCondition()创建,可以看做是Lock对象上的信号,类似于wait/notify
        Condition condition = lock.newCondition();
        int maxSize = 5;

        Producer producer = new Producer(queue, maxSize, lock, condition);
        Consumer consumer = new Consumer(queue, maxSize, lock, condition);

        Thread t1 = new Thread(producer);
        Thread t2 = new Thread(consumer);
        t1.start();
        t2.start();

    }


}
