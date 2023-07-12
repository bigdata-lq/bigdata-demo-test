package com.struct.current.pool;

import lombok.SneakyThrows;

import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Runnable没有返回值，Callable可以返回执行结果，是个泛型；
 * Callable接口的call()方法允许抛出异常；而Runnable接口的run()方法的异常只能在内部消化，不能继续上抛
 */
public class Test1 {

    static class Min implements Callable<Integer> {
        @Override
        public Integer call() throws Exception {
            Thread.sleep(1000);
            return 4;
        }
    }

    static class Max implements Runnable {
        @SneakyThrows
        @Override
        public void run() {
            Thread.sleep(1000);
        }
    }

    public static void main(String[] args) {
        ExecutorService executorService = Executors.newCachedThreadPool();
        executorService.submit(new Min());
        executorService.submit(new Max());
    }
}

