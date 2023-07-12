package com.struct.current.pool;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;


/**
 * CompletableFuture能够将回调放到与任务不同的线程中执行，
 * 也能将回调作为继续执行的同步函数，在与任务相同的线程中执行。
 * 它避免了传统回调最大的问题，那就是能够将控制流分离到不同的事件处理器中。
 * CompletableFuture弥补了Future模式的缺点。
 * 在异步的任务完成后，需要用其结果继续操作时，无需等待。
 * 可以直接通过thenAccept、thenApply、thenCompose等方式将前面异步处理的结果交给另外一个异步事件处理线程来处理。
 *
 */
public class CompletableFutureTest1 {
    public static void main(String[] args) {
        //可以自定义线程池
        ExecutorService executor = Executors.newCachedThreadPool();
        //runAsync的使用
        CompletableFuture<Void> runFuture = CompletableFuture.runAsync(() -> System.out.println("run,shawn"), executor);
        //supplyAsync的使用
        CompletableFuture<String> supplyFuture = CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(30000);
            } catch (Exception e) {
                e.printStackTrace();
            }
            System.out.print("supply,shawn");
            return "shawn"; }, executor);
        //runAsync的future没有返回值，输出null
        System.out.println(runFuture.join());
        //supplyAsync的future，有返回值
        System.out.println(supplyFuture.join());//必须等待数据返回
        System.out.println("主线程执行完毕");
        executor.shutdown(); // 线程池需要关闭
    }

}
