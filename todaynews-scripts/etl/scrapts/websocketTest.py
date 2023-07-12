
import time
import json
import pandas as pd
import requests
import websocket
from requests.adapters import HTTPAdapter
import time

try:
    import thread
except ImportError:
    import _thread as thread


class websocket_class :
    def __init__(self):
        pass

    #这里就是websocket爬虫的核心，发送请求，接收数据并做最后处理，
    def on_message(self,ws, message):
        print(message)
        pass

    def on_error(self,ws, error):
        print(error)
    #关闭websocket长连接
    def on_close(self,ws):
        print("关闭连接")

    #程序运行第一步
    def on_open(self,ws):
        def run(*args):
            #这里面就是写大家倒退出来页面请求第一步的代码
            pass
        thread.start_new_thread(run, ())


if __name__ == "__main__":
    print("-----------------------")
    # header = {
    #     'Accept-Encoding': 'gzip, deflate, br',
    #     'Accept-Language': 'zh-CN,zh;q=0.9,',
    #     'Cache-Control': 'no-cache',
    #     'Connection': 'Upgrade',
    #     'Cookie': cookie,
    #     'Host': 'ws-nextbi.yushanfang.com',
    #     'Origin': 'https://nextbi.yushanfang.com',
    #     'Pragma': 'no-cache',
    #     'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
    #     #这个参数要进行实时修改
    #     'Sec-WebSocket-Key': 'QBn6rnK29DZL6BC6+O2TRA==',
    #     'Sec-WebSocket-Version': '13',
    #     'Upgrade': 'websocket',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    # }
    #
    # websocket.enableTrace(True)
    # websocket_obj = websocket_class(cookie, appId, cateId,filename)
    # ws = websocket.WebSocketApp("wss://ws01.netlobbybattle.com:6899/",
    #                             on_message = websocket_obj.on_message,
    #                             on_error = websocket_obj.on_error,
    #                             on_close = websocket_obj.on_close,
    #                             header=header)
    #
    # ws.on_open = websocket_obj.on_open
    # ws.run_forever()
