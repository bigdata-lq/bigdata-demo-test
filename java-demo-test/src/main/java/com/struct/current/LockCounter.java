package com.struct.current;

import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;
import java.util.stream.IntStream;

/**
 * 用锁原则
 *      * 1. 只在更新对象的成员变量时加锁
 *      * 2. 只在访问可变的成员变量时加锁
 *      * 3. 不在调用其他对象的方法时加锁
 *      * 4. 降低锁范围：锁定代码的范围、作用域
 *      * 5. 细分锁粒度：一个大锁，拆分成多个小锁
 */
public class LockCounter {

    private int sum = 0;
    //可重入锁 公平锁  synchronized相同功能
    private Lock lock = new ReentrantLock(true);

    //cas 算法保证了原子性
    public static AtomicInteger atomicInteger   = new AtomicInteger(0);

    //主内存的可见性 只能保证主内存在读取数据一致
    public static volatile int num;

    public int incrAndGet(){
        try {
            lock.lock();
            return  ++ sum ;
        } finally {
            lock.unlock();
        }
    }

    public int getSum(){
        return sum;
    }

    public static void main(String[] args) {
        int loopNum = 10_0000;
        LockCounter counter = new LockCounter();
        // 从0到loopNum产生递增值序列,转成一个流，然后循环遍历0到loopNum数,进行求和
        IntStream.range(0, loopNum).parallel()
                .forEach(i -> counter.incrAndGet());
        System.out.println("counter.getSum() = " + counter.getSum());

        IntStream.range(0, loopNum).parallel()
                .forEach(i -> atomicInteger.incrementAndGet());

        System.out.println(atomicInteger.get());

        IntStream.range(0, loopNum).parallel()
                .forEach(i -> num++);

        System.out.println(num);
    }
}

