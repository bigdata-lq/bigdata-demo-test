
from hdfs.client import Client



if __name__ == '__main__':
    client = Client(url="http://pre-hadoop-master002:50070/")
    client.makedirs("/tmp/test")
    print(client.list("/tmp"))
    # print(client.delete("/tmp/test"))
    # client.upload("/tmp/test","D:\\code\\code20181219\\alading-bigdata-todaynews\\todaynews-scripts\\etl\\hivetable.sql")


    dt ='1112222\n'
    client.write(hdfs_path='/tmp/test/aaa',data=dt,overwrite=False, append=True)

    # print(client.list("/"))
    # with client.read("/tmp/test/foo.txt") as reader:
    #     print(reader.read())