
import redis

poolOne = redis.ConnectionPool(host='r-bp1z2upwcytw1t7yjh.redis.rds.aliyuncs.com',
                            port=6379, db=1,
                            password= 'kwW2eZp8PvxLIiPf')

poolTwo = redis.ConnectionPool(host='r-bp1v8dka8y7vd1rybr.redis.rds.aliyuncs.com',
                               port=6379, db=1,
                               password= 'Sye32OhBKymVEQcT')

rOne = redis.Redis(connection_pool=poolOne)
rTwo = redis.Redis(connection_pool=poolTwo)

## 日订单数据 旧key:
keys = rOne.keys('reco_rt:20200630:rt:feature:shop:*')
# keys = rOne.keys('reco_rt:20200630:rt:feature:shop5cate:*')


print("key的数量为{num}".format(num = len(keys)))

diffList= []

for oneKey in keys:
    resOne = rOne.hget(oneKey,'cnt_shop_click')
    resTwo = rTwo.hget(oneKey, 'cnt_shop_click')
    # resOne = rOne.hget(oneKey,'cnt_cate_order')
    # resTwo = rTwo.hget(oneKey, 'cnt_cate_order')


    ### 比较
    if resOne != resTwo:
        diffList.append(oneKey)
        print(oneKey, resOne, oneKey, resTwo)

print("统计结果不符合的数量为{num}, 不符合概率为{result},不符合key为{diffList}"
      .format(num = len(diffList),
              result = round(len(diffList)/ len(keys),4),
              diffList = diffList))







