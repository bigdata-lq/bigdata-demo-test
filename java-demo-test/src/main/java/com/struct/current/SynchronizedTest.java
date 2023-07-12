package com.struct.current;

import org.openjdk.jol.info.ClassLayout;


import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

public class SynchronizedTest  {

    /**
     * synchronized
     * 缺点：1.同步块的阻塞无法中断，不能Interruptibly
     *      2.无法自动解锁  wait、notify可以看做加锁和解锁
     *      3.不能知道是否可以立即拿到锁
     *
     *
     * 锁标识位 00 偏向锁 01 00 轻量级锁 10 重量级锁
     * @param args
     * @throws InterruptedException
     */

    public static void main(String[] args) throws InterruptedException {
            Object lightObject = new Object();
            //线程池
            final ThreadPoolExecutor executor = (ThreadPoolExecutor)Executors.newFixedThreadPool(5);
            //无锁状态
            System.out.println(ClassLayout.parseInstance(lightObject).toPrintable());
        /**
         * 循环次数位为1，锁标识01 偏向锁（独占）
         * 循环次数位大于1， 轻量级锁、重量级锁、独占锁都有可能
         */
        for (int i=0;i<3;i++) {
                executor.execute(new Runnable() {
                    @Override
                    public void run() {
                        synchronized (lightObject) {
                            // 锁标记存放在Java对象头的Mark Word中
                            System.out.println("线程id为" + Thread.currentThread().getId() + ",竞争轻量级锁：" + ClassLayout.parseInstance(lightObject).toPrintable());
                            try {
                                Thread.sleep(300);
                            } catch (InterruptedException e) {
                                e.printStackTrace();
                            }
                            System.out.println("线程id为" + Thread.currentThread().getId() + ",释放锁时间为" + getNowDate());
                        }

                    }
                });
            }

        executor.shutdown(); //等所有任务执行完再停止
        while (!executor.isTerminated()){ //主线程一直等待任务完成
            System.out.println("主线程" + Thread.currentThread().getName() +"一直等待任务完成");
            Thread.sleep(1000);
        }
        System.out.println("Good Bye!");
        }

    public static String getNowDate(){
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss"); //线程不安全，每次新建一个
        return dateFormat.format(new Date());
    }
}
