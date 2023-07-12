from paramiko import SSHClient
from paramiko import AutoAddPolicy
from etl.settings import hive_settings,spark_settings

class MySSHClient(SSHClient):

    def __init__(self,flag = False):
        #初始化SSH、时间对象
        super().__init__()
        self.set_missing_host_key_policy(AutoAddPolicy())#允许连接不在know_hosts文件中的主机
        if flag:
            self.connect(hostname=spark_settings['hostname'], port=spark_settings['port'],
                        username=spark_settings['username'], password=spark_settings['password'])
        else:
            self.connect(hostname=hive_settings['hostname'], port=hive_settings['port'],
                        username=hive_settings['username'], password=hive_settings['password'])

    def run(self, command):
        """
        :param command: 执行脚本
        :return:
        """
        stdin, stdout, stderr = self.exec_command(
            command, bufsize=-1
        )
        for l in self.line_buffered(stderr):
            print(l.strip("\n"))

        return stdout.read().decode('utf-8')


    def line_buffered(self,f):
        line_buf = ""
        while not f.channel.exit_status_ready():
            line_buf += f.readline()
            if line_buf.endswith('\n'):
                yield line_buf
                line_buf = ''