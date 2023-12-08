from typing import Union, Any
import paramiko


def _ssh_client():
    return paramiko.SSHClient()
# ssh.connect(hostname, username=username, key_filename=key_path, password=passphrase)


class SSHConnector:
    _missing_host_key_policy = paramiko.AutoAddPolicy()
    _private_key = ""
    def __init__(self, hostname, usernmae, password: Union[str, None] = None, port: int = 22, **kwargs: Any):
        self.client = _ssh_client()
        self.hostname = hostname
        self.username = usernmae
        self.password = password
        self.port = port
        if kwargs.get("auto_add", False) == True:
            self.client.set_missing_host_key_policy(self._missing_host_key_policy)
    def connect(self):
        self.client.connect(hostname=self.hostname, port=self.port,username=self.username, password=self.password)
