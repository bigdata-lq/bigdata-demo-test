#logging日志打印模块

import logging
from etl.testing.lqTest.dataconfig.project_path import * #导入dataconfig.project_path 中的全部内容

class MyLog:
    def my_log(self,msg,level):
       ###1 定义一个日志收集器（logging.getLogger(name)方法进行初始化）my_logger日志对象（理解成 my_logger容器）
        my_logger = logging.getLogger()
        # 设定级别   收集和输出不指定级别会默认收集和输出warning级别以上的 （setLevel设置日志等级）
        #debug<info<warn<Error<Fatal #如果把loger的级别设置为INFO， 那么小于INFO级别的日志都不输出， 大于等于INFO级别的日志都输出
        my_logger.setLevel("DEBUG")
        # 设置日志输出格式
        formatter = logging.Formatter(
            "%(asctime)s -%(levelname)s - %(filename)s[line:%(lineno)d] %(levelname)s-日志信息：%(message)s")

        ###2 创建输出渠道

        # 创建一个（我们自己）的输出渠道，使用StreamHandler方法（输出日志）        -控制台
        ch = logging.StreamHandler()
        ch.setLevel("DEBUG")
        #日志输出格式
        ch.setFormatter(formatter)
        #####  3  指定输出的位置 FileHandler 输出到哪里
        # 指定输出到文件（logging.FileHandler追加写入到磁盘文件）
        fh = logging.FileHandler(log_path, encoding="utf-8")
        fh.setLevel("DEBUG")
        fh.setFormatter(formatter)

        # 两者对接 （过程连接“接水管”）
        my_logger.addHandler(ch)
        my_logger.addHandler(fh)

        ###4  收集日志（判断语句）（操作过程）
        if level == "DEBUG":
            my_logger.debug(msg)
        elif level == "INFO":
            my_logger.info(msg)
        elif level == "WARNING":
            my_logger.warning(msg)
        elif level == "ERROR":
            my_logger.error(msg)
        elif level == "CRITICAL":
            my_logger.critical(msg)


        #关闭日志收集器  不关闭会重复打印日志  (一个方法一个方法调用，到关闭日志收集器结束，开始新的一轮)
        my_logger.removeHandler(ch)
        my_logger.removeHandler(fh)

    # 日志的5个级别对应5个函数
    def debug(self,msg):
        self.my_log(msg,"DEBUG")

    def info(self,msg):
        self.my_log(msg,"INFO")

    def warning(self,msg):
        self.my_log(msg,"WARNING")

    def error(self,msg):
        self.my_log(msg,"ERROR")

    def critical(self,msg):
        self.my_log(msg,"CRITICAL")


if __name__ == '__main__':
    #创建类的对象
    my_logger = MyLog()
    my_logger.debug("1")
    my_logger.info("2")
    my_logger.error("3")


    #1、调用那个方法(赋值)对应的进入到那个方法走一遍，然后进去到my_log到收集日志到关闭日志收集器（结束），在重新开始调用