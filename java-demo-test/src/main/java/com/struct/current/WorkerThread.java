package com.struct.current;

/**
 * @description:
 * @author: liquan
 * @time: 2022/11/24 0024 上午 10:24
 */
public class WorkerThread implements Runnable {

    private String s;

    public WorkerThread(String s) {
        this.s = s;
    }

    @Override
    public void run() {
        System.out.println(Thread.currentThread().getName() + " (Start) message : " + s);
        processCommand();
        System.out.println(Thread.currentThread().getName() + " (End)");
    }

    private void processCommand() {
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }


}
