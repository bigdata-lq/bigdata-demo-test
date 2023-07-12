package com.struct.current.pool;

import java.util.concurrent.CompletableFuture;

/**
 * thenRun/thenRunAsync
 * 做完第一个任务后，再做第二个任务。某个任务执行完成后，执行回调方法；
 * 但是前后两个任务没有参数传递，第二个任务也没有返回值
 *
 * thenAccept/thenAcceptAsync
 * 第一个任务执行完成后，执行第二个回调方法任务，会将该任务的执行结果，作为入参，传递到回调方法中，
 * 但是回调方法是没有返回值的。
 *
 * thenApply/thenApplyAsync
 * 第一个任务执行完成后，执行第二个回调方法任务，会将该任务的执行结果，作为入参，传递到回调方法中，
 * 并且回调方法是有返回值的。
 *
 * 注意：上述三个方法如果执行第一个任务的时候，传入了一个自定义线程池：
 * 调用xxx方法执行第二个任务时，则第二个任务和第一个任务是共用同一个线程池。
 * 调用xxxAsync执行第二个任务时，则第一个任务使用的是你自己传入的线程池，第二个任务使用的是ForkJoin线程池
 */
public class CompletableFutureTest2 {

    //举个例子
    public static void main(String[] args) throws Exception {
        CompletableFuture<String> orgFuture = CompletableFuture.supplyAsync(
                ()->{
                    System.out.println("原始CompletableFuture方法任务");
                    try {
                        Thread.sleep(300l);
                        System.out.println(Thread.currentThread().getName());
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    return "shawn";
                }
        );
        CompletableFuture<String> thenApplyFuture = orgFuture.thenApply((a) -> {
            System.out.println(Thread.currentThread().getName());
            if ("shawn".equals(a)) {
                return "确实很帅";
            }
            return "考虑考虑";
        });

        System.out.println(thenApplyFuture.get());
    }

}
