package com.struct.current;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

/**
 * @description:
 * 1.守护队列监听线程池内部队列的情况
 * 2.shutdown shutdownNow的区别
 * 3.线程的基础知识
 * @author: liquan
 * @time: 2022/11/24 0024 上午 10:24
 */
public class doFixThreadPool {

    public static void main(String[] args) throws InterruptedException {

        final ThreadPoolExecutor executor = (ThreadPoolExecutor)Executors.newFixedThreadPool(5);
        final DaemonThread daemonThread = new DaemonThread(executor); //守护线程，用来监听线程内队列的情况
        daemonThread.setDaemon(true);
        daemonThread.start();

        for (int i = 0; i < 10; i++) {
            Runnable worker = new WorkerThread("" + i);
            executor.execute(worker);
        }

        executor.shutdown(); //等所有任务执行完再停止
        while (!executor.isTerminated()){ //主线程一直等待任务完成
            System.out.println("主线程" + Thread.currentThread().getName() +"一直等待任务完成");
            Thread.sleep(1000);
        }
        System.out.println("Good Bye!");
    }

}
