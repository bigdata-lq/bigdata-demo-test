package com.struct.current.pool;


import lombok.extern.slf4j.Slf4j;

import java.io.IOException;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * newCachedThreadPool 适用场景：快速处理大量耗时较短的任务，如 Netty 的 NIO 接受请求时，可使用
 * newFixedThreadPool 固定线程池
 * newScheduledThreadPool 可执行延迟的线程池
 * newSingleThreadExecutor 单一线程池
 * 自定义线程池
 */
@Slf4j
public class ThreadPoolTest {

    public static void main(String[] args) throws Exception {
        BlockingQueue<Runnable> workQueue = new ArrayBlockingQueue<>(2); //排队队列
        NameThreadFactory threadFactory = new NameThreadFactory();
        RejectedExecutionHandler handler = new MyIgnorePolicy();

        //默认线程工程 Executors.defaultThreadFactory()
        //默认拒绝策略 new ThreadPoolExecutor.AbortPolicy()
        ThreadPoolExecutor executor = new ThreadPoolExecutor(2, 4, 2000, TimeUnit.MILLISECONDS,
                workQueue, threadFactory,  handler);
        // 预启动所有核心线程
        executor.prestartAllCoreThreads();
//        executor.prestartCoreThread();

//        Thread.sleep(100000l);

        for (int i = 1; i <= 10; i++) {
            MyTask task = new MyTask(String.valueOf(i));
            executor.execute(task);
        }
        System.in.read();//阻塞主线程

    }

    /**
     * 自定义线程名称
     */
    static class NameThreadFactory implements ThreadFactory {
        // 原子性 可见性 顺序性
        private final AtomicInteger mThreadNum = new AtomicInteger(1);

        @Override
        public Thread newThread(Runnable r) {
            Thread t = new Thread(r, "my-thread-" + mThreadNum.getAndIncrement());
            System.out.println(t.getName() + " has been created");
            return t;
        }
    }

    /**
     * 自定义拒绝线程处理逻辑
     */
    static class MyIgnorePolicy implements RejectedExecutionHandler {
        @Override
        public void rejectedExecution(Runnable r, ThreadPoolExecutor executor) {
            doLog(r, executor);
        }

        private void doLog(Runnable r, ThreadPoolExecutor e) {
            // 可做日志记录等
            System.err.println( r.toString() + " rejected");
            System.out.println("completedTaskCount: " + e.getCompletedTaskCount());
        }
    }

    static class MyTask implements Runnable {
        private String name;

        public MyTask(String name) {
            this.name = name;
        }

        @Override
        public void run() {
            try {
                System.out.println(this.toString() + " is running!");
                // 让任务执行慢点
                Thread.sleep(3000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        public String getName() {
            return name;
        }

        @Override
        public String toString() {
            return "MyTask [name=" + name + "]";
        }
    }

}
