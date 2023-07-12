package com.struct.current;

import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.LockSupport;

public class LockSupportTest {

    /**
     * 专门处理执行代码的本线程
     * @param args
     */
    public static void main(String[] args) {

        Thread t1 = new Thread(() -> {
            System.out.println(Thread.currentThread().getName() + " 开始执行");
            LockSupport.park();
            System.out.println(Thread.currentThread().getName() + " 被唤醒");
        }, "t1");
        t1.start();

        new Thread(() -> {
            System.out.println(Thread.currentThread().getName() + " 开始执行");
            try {
                TimeUnit.SECONDS.sleep(5);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
            System.out.println(Thread.currentThread().getName() + " 开始唤醒");
            LockSupport.unpark(t1);
        }, "t2").start();
    }

}
