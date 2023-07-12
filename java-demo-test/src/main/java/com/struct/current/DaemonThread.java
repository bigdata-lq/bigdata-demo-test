package com.struct.current;

import lombok.extern.slf4j.Slf4j;

import java.util.concurrent.ThreadPoolExecutor;

/**
 * @description:
 * @author: liquan
 * @time: 2022/11/24 0024 上午 11:55
 */
@Slf4j
public class DaemonThread extends Thread {

    private ThreadPoolExecutor executor ;

    public DaemonThread(ThreadPoolExecutor executor) {
        this.executor = executor ;
    }

    @Override
    public void run() {
        while (true){
            log.info("executor running size is {}, waiting size is {}", executor.getActiveCount(), executor.getQueue().size());
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
