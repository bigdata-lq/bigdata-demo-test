package com.struct.current.pool;

import org.junit.jupiter.api.Test;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;


public class CompletableFutureTest4 {

    /**
     * 多线程之间传参数,有返回值
     * @throws ExecutionException
     * @throws InterruptedException
     */
    @Test
    public void thenAppliyTest() throws ExecutionException, InterruptedException {
        CompletableFuture<String> future = CompletableFuture
                .supplyAsync(()->"hello") //线程1
                .thenApplyAsync(w->w + " world\n") //线程2
                .thenApplyAsync(w->w+" 真有意思\n") //线程3
                .thenApplyAsync(String::toUpperCase) //线程4
                ;
        System.out.println(future.get());
    }

    @Test
    public void thenAcceptTest() throws ExecutionException, InterruptedException {
        CompletableFuture<Void> future = CompletableFuture
                .supplyAsync(()->"hello") //线程1
                .thenAccept(w-> System.out.println(w.concat("world"))) //没有返回值
//                .thenApplyAsync(w->w+" 真有意思\n") //线程3
//                .thenApplyAsync(String::toUpperCase) //线程4
                ;
        System.out.println(future.get());
    }

    /**
     * 线程1 线程2执行完了，执行线程3
     * @throws ExecutionException
     * @throws InterruptedException
     */
    @Test
    public void thenAcceptBothTest() throws ExecutionException, InterruptedException {
        CompletableFuture<String> future = CompletableFuture.supplyAsync(()->{ //线程1
            return "hello";
        }); //线程1
        CompletableFuture<String> future1 = CompletableFuture.supplyAsync(()->{ //线程2
            return "world";
        }); //线程2
        System.out.println(future.get()); // get 和 join 均会阻塞线程
        System.out.println(future1.get());

        //线程3 没有返回值
        future1.thenAcceptBoth(future,(a,b)->{System.out.println(b+a+"真有意思");}); //线程3
        //线程4 有返回值
        CompletableFuture<String> result = future1.thenCombine(future, (a, b) -> a + b);
        System.out.println(result.get()); //get和join区别 异常的处理点不同
        System.out.println(result.join());

    }
}
