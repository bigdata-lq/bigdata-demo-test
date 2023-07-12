package com.struct.current.pool;

import org.junit.jupiter.api.Test;

import java.util.Random;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.function.BiConsumer;
import java.util.function.Function;
import java.util.function.Supplier;

import static java.lang.Thread.sleep;

/**
 * exceptionally
 * 某个任务执行异常时，执行的回调方法;并且有抛出异常作为参数，传递到回调方法
 * whenComplete
 * 某个任务执行完成后，执行的回调方法，无返回值；并且whenComplete方法返回的CompletableFuture的result是上个任务的结果
 * handle
 *
 * 某个任务执行完成后，执行回调方法，并且是有返回值的;并且handle方法返回的CompletableFuture的result是回调方法执行的结果
 */
public class CompletableFutureTest3 {

    @Test
    public void handleTest() throws ExecutionException, InterruptedException {
        //举例
        CompletableFuture<String> orgFuture = CompletableFuture.supplyAsync(
                ()->{
                    System.out.println("当前线程名称：" + Thread.currentThread().getName());
                    try {
                        sleep(2000L);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    return "shawn";
                }
        );
        //exceptionally使用方法是orgFuture.exceptionally((e)->{...})
        CompletableFuture<String> rstFuture = orgFuture.handle((a, throwable) -> {

            System.out.println("上个任务执行完啦，还把" + a + "传过来");
            if ("shawn".equals(a)) {
                try {
                    sleep(2000L);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("666");
                //whenComplete没有返回
                return "好帅啊";
            }
            System.out.println("233333");
            return null;
        });
        System.out.println("主线程继续执行");
        System.out.println(rstFuture.get());
    }


    @Test
    public void completeTest() throws Exception {
        System.out.println("本方法所用线程 " + Thread.currentThread().getName());
        ExecutorService threadPool = Executors.newFixedThreadPool(3);
        //一个5秒任务
        Supplier<String> supplier = () -> {
            try {
                sleep(5);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            String s = "supplier " + Thread.currentThread().getName();
            System.out.println(s);
            return s;
        };
        //任务完成后的行为
        BiConsumer<Object, Throwable> action = (result, exception) -> {
            String s = "action " + Thread.currentThread().getName();
            System.out.println(result + s);
            return;
        };

        //将任务交给线程池处理,任务结束会自动调用CompletableFuture.complete()方法。
        CompletableFuture<String> future1 = CompletableFuture.supplyAsync(supplier, threadPool);
        //睡1秒，这时任务还没结束，这时调用whenComplete方法，将会和supplier的执行使用相同的线程。
        sleep(1);
        CompletableFuture future2 = future1.whenComplete(action);
        System.out.println(future2.get());

        //睡10秒，这时任务已结束，这时调用whenComplete方法。只能使用调用本方法的线程
        sleep(10);
        CompletableFuture future3 = future1.whenComplete(action);
        System.out.println(future3.get());

        sleep(100);

    }

    @Test
    public void exceptionallyTest() throws Exception {
        CompletableFuture<Double> future = CompletableFuture.supplyAsync(() -> {

                if (Math.random() < 0.5) {
                    throw new RuntimeException("抛出异常");
                }

                System.out.println("正常结束");
                return 1.1;
            }).thenApply(result -> {

                System.out.println("thenApply接收到的参数 = " + result);
                return result;
            }).exceptionally(new Function<Throwable, Double>() { //异常处理
                @Override
                public Double apply(Throwable throwable) {
                    System.out.println("异常：" + throwable.getMessage());
                    return 0.0;
                }
            });

            System.out.println("最终返回的结果 = " + future.get());

        }

        @Test
        public void testAllof(){

                ExecutorService executorService = Executors.newFixedThreadPool(4);
            Random random = new Random();
            long start = System.currentTimeMillis();
                CompletableFuture<String> futureA = CompletableFuture.supplyAsync(() -> {
                    try {
                        Thread.sleep(1000 + random.nextInt(1000));
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    return "商品详情";
                },executorService);

                CompletableFuture<String> futureB = CompletableFuture.supplyAsync(() -> {
                    try {
                        Thread.sleep(1000 + random.nextInt(1000));
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    return "卖家信息";
                },executorService);

                CompletableFuture<String> futureC = CompletableFuture.supplyAsync(() -> {
                    try {
                        Thread.sleep(1000 + random.nextInt(1000));
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    return "库存信息";
                },executorService);

                CompletableFuture<String> futureD = CompletableFuture.supplyAsync(() -> {
                    try {
                        Thread.sleep(1000 + random.nextInt(1000));
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    return "订单信息";
                },executorService);

                CompletableFuture<Void> allFuture = CompletableFuture.allOf(futureA, futureB, futureC, futureD);
                allFuture.join();

                System.out.println(futureA.join() + futureB.join() + futureC.join() + futureD.join());
                System.out.println("总耗时:" + (System.currentTimeMillis() - start));
        }
}
