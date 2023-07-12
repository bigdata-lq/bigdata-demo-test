## -*-coding:utf-8 -*-
#---------
# Name:lq
# Message: 测试Hive
#---------


from impala.dbapi import connect
import base64
import binascii
url = "aHR0cHM6Ly93d3cuY25ibG9ncy5jb20vc29uZ3poaXh1ZS8="
url = "F4x2sYybShXHS8QBTtym6g=="
aaa = base64.b64encode(url.encode())
if None:
    print(aaa)
print(aaa)
# str_url = base64.b64decode(url).decode("utf-8")
# print(str_url)


def is_base64_code(s):
    '''Check s is Base64.b64encode'''
    if not isinstance(s ,str) or not s:
        raise binascii.Error('params s not string or None')

    _base64_code = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                    'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a',
                    'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                    't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1',
                    '2', '3', '4','5', '6', '7', '8', '9', '+',
                    '/', '=' ]

    # Check base64 OR codeCheck % 4
    code_fail = [ i for i in s if i not in _base64_code]
    if code_fail or len(s) % 4 != 0:
        return False
    return True


print(is_base64_code(url))
conn = connect(host='172.16.50.4', port=10001, user='hadoop', password='JafumRvMJwajbAP2', database='ytdw', auth_mechanism="PLAIN")
cur = conn.cursor()

cur.execute("desc dw_order_d")
d = cur.fetchall()
cols = []
for i in d:
    cols.append(i[0])

print(cols)
##ytdw.ods_t_cmc_shop_d.address
cur.execute("select address from ods_t_cmc_shop_d where dayid = '20200826' limit 1")
data = cur.fetchall()
for i in data:
    print(i[0])
    print(type(i))
