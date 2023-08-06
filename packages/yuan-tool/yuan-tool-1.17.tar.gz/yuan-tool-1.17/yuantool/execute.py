import paramiko
import os


class ExecuteLinuxShell:
    """
        执行linux shell命令
    """

    def __init__(self, hostname: str, port: int, username: str, password: str):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password

    def __int__(self):
        pass

    def create_remote_connection(self) -> bool:
        try:
            # 实例化SSHClient
            self.client = paramiko.SSHClient()
            # 自动添加策略，保存服务器的主机名和密钥信息
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)
            return True
        except Exception as e:
            print(e)
            return False

    def remote_exec(self, cmd):
        stdin, stdout, stderr = self.client.exec_command(cmd)
        return '\n'.join(stdout.readlines())

    @classmethod
    def local_exec(cls, cmd):
        try:
            result = os.popen(cmd)
            return '\n'.join(result.readlines())
        except Exception as e:
            print(e)
