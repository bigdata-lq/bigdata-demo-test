import unittest

from etl.testing.ly.libs.ddt import *
from etl.testing.ly.utils.read_json import ReadJson

moneyFlowData = ReadJson("money_flow_1.json").jsonCase
print(type(moneyFlowData))

@ddt
class testwork(unittest.TestCase):

    @data(*moneyFlowData)
    # @unpack
    def test_01(self,value):
        print(value)

    # @file_data(os.getcwd()+'/jsonll.txt')
    # def test_02(self,value2):
    #     print(value2)

if __name__ == '__main__':
    unittest.main()