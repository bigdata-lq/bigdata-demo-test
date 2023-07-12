package com.struct.current.pool;

import java.util.concurrent.*;

public class Test2 {

    public static void main(String[] args) throws ExecutionException, InterruptedException, TimeoutException {
        ExecutorService executor = Executors.newCachedThreadPool();
        //Lambda 是一个 callable， 提交后便立即执行，这里返回的是 FutureTask 实例
        Future<String> future = executor.submit(() -> {
            System.out.println("running task");
            Thread.sleep(5000);
            return "return task";
        });
        System.out.println("主线程做其他事情");
        Boolean flag = future.isDone();
        while (!flag){
            flag = future.isDone();
            Thread.sleep(100);
            System.out.println("等待异步线程执行完成");
        }
        String resutlt = future.get();

//        System.out.println(future.get(2, TimeUnit.SECONDS));
        System.out.println("返回结果为:" + resutlt);
        executor.shutdown(); //销毁线程池
    }

}
