#生成随机数/从某个列表中选择任一
import random  #随机模块
from faker import Factory
#faker来制造一些虚拟数据   Factory是类   （数据生成器）

#使用Factory.create  Factory调用create方法创建随机数
faker = Factory.create("zh-CN")
# print(faker.email())


class Generator:

    @staticmethod #静态方法
    def random_str( min_chars=8, max_chars=8):
        return faker.pystr(min_chars=min_chars,max_chars=max_chars)



    def factory_choice_generator(values):
        """ 返回一个生成器函数，调用这个函数产生生成器，从给定的list中随机取一项。 """
        def choice_generator():
            my_list = list(values)
            # rand = random.Random()
            while True:
                yield random.choice(my_list)
        return choice_generator

if __name__ == '__main__':
    #调用静态方法，不用实例化
    print(Generator.random_str())
