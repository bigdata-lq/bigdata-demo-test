package com.test.client;

import org.apache.spark.launcher.SparkAppHandle;
import org.apache.spark.launcher.SparkLauncher;

import java.io.IOException;
import java.util.HashMap;
import java.util.concurrent.CountDownLatch;

public class LanuncherAppDemo {


    public static void main(String[] args) throws Exception {
        HashMap env = new HashMap();
        //这两个属性必须设置
        env.put("HADOOP_CONF_DIR", "/usr/local/hadoop/etc/overriterHaoopConf");
        env.put("JAVA_HOME", "/usr/local/java/jdk1.8.0_151");
        //可以不设置
        //env.put("YARN_CONF_DIR","");
        CountDownLatch countDownLatch = new CountDownLatch(1);
        //这里调用setJavaHome()方法后，JAVA_HOME is not set 错误依然存在
        SparkAppHandle handle = new SparkLauncher(env)
                .setSparkHome("/usr/local/spark")
                .setAppResource("/usr/local/spark/spark-demo.jar")
                .setMainClass("com.learn.spark.SimpleApp")
                .setMaster("yarn")
                .setDeployMode("cluster")
                .setConf("spark.app.id", "11222")
                .setConf("spark.driver.memory", "2g")
                .setConf("spark.akka.frameSize", "200")
                .setConf("spark.executor.memory", "1g")
                .setConf("spark.executor.instances", "32")
                .setConf("spark.executor.cores", "3")
                .setConf("spark.default.parallelism", "10")
                .setConf("spark.driver.allowMultipleContexts", "true")
                .setVerbose(true).startApplication(new SparkAppHandle.Listener() {
                    //这里监听任务状态，当任务结束时（不管是什么原因结束）,isFinal（）方法会返回true,否则返回false
                    @Override
                    public void stateChanged(SparkAppHandle sparkAppHandle) {
                        if (sparkAppHandle.getState().isFinal()) {
                            countDownLatch.countDown();
                        }
                        System.out.println("state:" + sparkAppHandle.getState().toString());
                    }


                    @Override
                    public void infoChanged(SparkAppHandle sparkAppHandle) {
                        System.out.println("Info:" + sparkAppHandle.getState().toString());
                    }
                });
        System.out.println("The task is executing, please wait ....");
        //线程等待任务结束
            countDownLatch.await();
        System.out.println("The task is finished!");
    }
}
