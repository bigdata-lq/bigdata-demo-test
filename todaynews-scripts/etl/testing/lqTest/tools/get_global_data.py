from  etl.testing.lqTest.dataconfig.project_path import *
import pandas as pd #处理表格和混杂数据（设计）
from etl.testing.lqTest.tools.read_config import ReadConfig


from faker import Faker

f = Faker(locale='zh_CN')

"""
class GetData(object):
    Cookie = {"X-Token":"c12621bb09e969757e3c738d5dfc0be4","sidebarStatus":1}
    # 行减2，列减1（最小iloc[0,0]为A2）
    key001 = pd.read_excel(test_case_data_path,sheet_name="init").iloc[52,1]   # 实验
    key002 = pd.read_excel(test_case_data_path,sheet_name="init").iloc[53,1]   # 实验


    url = "union-uat.zgmmtuan.com"
    username="ceshi1"
    password ="123"
    port = "82"
    user_id = 2894774               # 下单人id
    product_id = 30
    money = 50000                   # 充值金额
    pay_password = 960329           # 支付密码
    num = 1                         # 购买sku的个数
    how_much_is_a_piece_worth = 2   # 一件为几单
    level_vip = 30          # 区代利润-->>1
    level_one = 30          # 县代利润-->>2
    level_two = 30          # 市代利润-->>3
    level_three = 30        # 省代利润-->>4
    level_four = 30         # 大区利润-->>5
    level_five = 30         # 分公司利润-->>6/7/8
    price = 50000           # 商品价格
    price_original = 50000
"""


class GetData:
    url = "shop.uat.zgmmtuan.com"
    houtai_url="admin.uat.zgmmtuan.com"
    port = "80"
    id =963224                    # 下单人id
    product_id = 30
    money = 50000                   # 充值金额
    pay_password = 960329           # 支付密码
    num = 1                         # 购买sku的个数
    how_much_is_a_piece_worth = 1   # 一件为几单
    price = 40000           # 商品价格
    price_original = 40000
    customer_id=963224
    account=5000
    telephone=18257058467


if __name__ == '__main__':
    # setattr(GetData,"Cookie","123456")
    print(test_case_data_path)
    print(getattr(GetData,"Cookie"))
    print(hasattr(GetData,"Cookie"))
    print(getattr(GetData,"key001"))
    print(getattr(GetData,"key002"))    # 实验
    print(getattr(GetData,"user_id"))




