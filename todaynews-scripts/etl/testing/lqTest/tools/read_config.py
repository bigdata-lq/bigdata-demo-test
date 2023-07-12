#tools/read_config/读取配置文件时注意读取的类型正确性

import configparser#作用读取配置文件
from etl.testing.lqTest.dataconfig.project_path import *
from configparser import NoSectionError,NoOptionError

#创建ConfigParser类对象
cf = configparser.ConfigParser()


#打开配置文件函数 ，read 函数打开文件类似于open，如果有中文最好设置成UTF-8  config_path 配置路径
cf.read(config_path,encoding="utf-8")


#读取配置文件中的内容，进行值的返回（获取想要的值）
class ReadConfig:
    # @staticmethod 静态方法 （同一类方法下的普通方法（参数自己传））
    @staticmethod
    #get(section,option) —得到section（.ini）中option的值，返回为string类型
    def get_http(option:str):
        #把cf配置路径文件中的 section 和  option 值取出来（用get方法） 注意option类型为str
        return cf["HTTP"][option]


    @staticmethod
    def get_sql():
        return cf["DB"]["db_config"]


    @staticmethod
    def get_test_data(col_name:str):
        return cf["DATA"][col_name]


    @staticmethod
    def get_regx():
        return cf["REGX"]["PATTERN"]


    @staticmethod
    def get_case_run():
        return cf["MODE"]["mode"]

    @staticmethod
    def get_mysql_connect(option:str):

        return cf["DBXUKAI"][option]


# 通用改造？



    def __init__(self, filename):
        try:
            cf = configparser.ConfigParser()
            # self.filename = filename
            cf.read(filename, encoding='utf-8')
        except Exception as e:
            raise e

    def get_all_option(self, section):
        """获取指定section下所有的option"""
        try:
            options = cf.options(section)
            return options
        except NoSectionError:
            print('NoSectionError : {} not exist'.format(section))
        except Exception as e:
            raise e

    def get_value(self, section):
        """获取指定section中所有的option和value，返回一个字典"""
        try:
            value = dict(cf.items(section))
            return value
        except (NoSectionError, KeyError):
            print('{} not exist'.format(section))
        except Exception as e:
            raise e

    def get_option_value(self,section, option, flag=False):
        """
        获取指定section和option对应的数据
        如果option对应数据为数字，则自动转换为int或者float
        如果option对应的数据是个可以使用eval转换的类型，则传递flag为True时，自动转换,否则输出str
        """
        try:
            value = cf.get(section, option)
            if value.isdigit():
                return int(value)
            try:
                return float(value)
            except Exception:
                pass
            if isinstance(flag, bool) and flag:
                return eval(value)
            return value
        except (NoSectionError, NoOptionError, KeyError):
            print('no option "{}" or section "{}"'.format(option, section))
        except Exception as e:
            raise e


    def __call__(self, section='DEFAULT', option=None, flag_eval=False, flag_bool=False):
        """
        对象当成函数使用的时候会默认调用这个方法
        这个方法可以实现上面多数功能
        :param section:
        :param option:
        :param flag_eval: 如果为True 我们使用eval转换类型
        :param flag_bool: 如果为True 我们使用把数据转换为bool
        :return:
        """
        if option is None:
            return dict(self[section])
        if isinstance(flag_bool, bool):
            if flag_bool:
                return self.getboolean(section, option)
        else:
            raise ValueError('{} must be type bool'.format(flag_bool))
        data = self.get(section, option)
        if data.isdigit():
            return int(data)
        try:
            return float(data)
        except Exception:
            pass
        if isinstance(flag_eval, bool):
            if flag_eval:
                return eval(data)
        else:
            raise ValueError('{} must be type bool'.format(flag_eval))
        return data


if __name__ == '__main__':
    from etl.testing.lqTest.dataconfig.project_path import *
    # rd = ReadConfig("E:\Program Files (x86)\download\APItest_unittest_cmp-master\dataconfig\config.ini")
    # case_config = rd.read_config(case_config_path,"MODE","mode")
    # print(case_config)
    #打印具体读取congfig中的值
    print(type(ReadConfig.get_mysql_connect("user")))
    print(ReadConfig.get_http("port"))
    print(ReadConfig.get_sql())
    print(ReadConfig.get_test_data("json_path"))
    print(ReadConfig.get_regx())
    print(type(ReadConfig.get_test_data("module")))

    print(cf.options("DATA"))
    print(cf.items("DATA"))
    rd = ReadConfig("E:\Program Files (x86)\download\APItest_unittest_cmp-master\dataconfig\config.ini")

    case_id =rd.get_option_value("DATA","case_id")
    options =rd.get_all_option("DATA")
    value = rd.get_value("DATA")
    print(case_id)
    print(type(case_id))
    print(options)
    print(value)
    print(ReadConfig.get_test_data("json_path"))
    # print(ReadConfig.get_test_data(col_name="case_id"),type(ReadConfig.get_test_data(col_name="case_id")))
