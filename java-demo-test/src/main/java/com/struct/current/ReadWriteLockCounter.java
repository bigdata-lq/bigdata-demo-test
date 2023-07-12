package com.struct.current;

import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;
import java.util.stream.IntStream;

/**
 * 一个读锁，一个写锁。它适用于读多写少的并发情况
 * 适用于读多写少的场景,hdfs的源代码应用比较广泛
 */
public class ReadWriteLockCounter {
    private int sum = 0;
    /**
     * 可重入、读写锁、公平/非公平锁
     * fair：true:公平锁 false:非公平锁
     * 公平锁意味排队靠前的优先
     * 非公平锁则都是同样机会
     */
    private ReadWriteLock lock = new ReentrantReadWriteLock(true);

    public int incrAndGet() {
        try {
            // 写锁 独占锁 被读锁排斥
            lock.writeLock().lock();
            return ++sum;
        } finally {
            lock.writeLock().unlock();
        }
    }

    public int getSum() {
        try {
            // 读锁 共享锁 保证可见性
            lock.readLock().lock();
            return sum;
        } finally {
            lock.readLock().unlock();
        }
    }

    public static void main(String[] args) {
        int loopNum = 10_0000;
        ReadWriteLockCounter readWriteLockCounter = new ReadWriteLockCounter();
        // 从0到loopNum产生递增值序列,转成一个流，然后循环遍历0到loopNum数,进行求和
        IntStream.range(0, loopNum).parallel()
                .forEach(i -> readWriteLockCounter.incrAndGet());
        System.out.println("counter.getSum() = " + readWriteLockCounter.getSum());
        System.out.println("counter.getSum() = " + readWriteLockCounter.getSum());
    }
}

