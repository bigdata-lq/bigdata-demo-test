package com.struct.current.pool;

import java.util.concurrent.*;

/**
 *  线程池十个坑
 *  https://mp.weixin.qq.com/s?__biz=MzkyMzU5Mzk1NQ==&mid=2247506583&idx=1&sn=ea77e7d3d7ef8ded514e56c6b907f9d4&source=41#wechat_redirect
 *  AbortPolicy: 丢弃任务并抛出RejectedExecutionException异常。(默认拒绝策略)
 * DiscardPolicy：丢弃任务，但是不抛出异常。
 * DiscardOldestPolicy：丢弃队列最前面的任务，然后重新尝试执行任务。
 * CallerRunsPolicy：由调用方线程处理该任务
 */
public class DiscardThreadPoolTest {

    public static void main(String[] args) throws ExecutionException, InterruptedException, TimeoutException {
        // 一个核心线程，队列最大为1，最大线程数也是1.拒绝策略是DiscardPolicy
        ThreadPoolExecutor executorService = new ThreadPoolExecutor(1, 1, 1L, TimeUnit.MINUTES,
                new ArrayBlockingQueue<>(1), new ThreadPoolExecutor.DiscardPolicy());

        Future f1 = executorService.submit(()-> {
            System.out.println("提交任务1");
            try {
                Thread.sleep(3000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        });

        Future f2 = executorService.submit(()->{
            System.out.println("提交任务2");
        });

        Future f3 = executorService.submit(()->{
            System.out.println("提交任务3");
        });

        System.out.println("任务1完成 " + f1.get());// 等待任务1执行完毕
        System.out.println("任务2完成" + f2.get());// 等待任务2执行完毕
//        System.out.println("任务3完成" + f3.get());// 等待任务3执行完毕 此时主线程会卡死
        System.out.println("任务3完成" + f3.get(3, TimeUnit.SECONDS)); // 超时


        executorService.shutdown();// 关闭线程池，阻塞直到所有任务执行完毕
    }
}
