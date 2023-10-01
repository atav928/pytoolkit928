"""Create a custo CA."""

import tempfile, certifi, os
from pathlib import Path
from pytoolkit.static import ENCODING

class CustomCa:
    CUSTOM_CA = """adsfdslkfakfjalksdjfadfad \
                    asdfflkdjskfajdsfjadsklfdsfa\
                    adsfsdsdfkjdfjasdkfjadsjflads"""
    def __init__(self, cafile, capath=None):
        self.cafile = cafile
        if not self.check_cafiles(self.cafile):
            raise FileExistsError

        self.capath = capath
        if self.capath:
            self.set_certpath(self.capath)
        else:
            self.CERT_PATH = tempfile.gettempdir()

        self.create_ca()
        self.set_env()

    def set_certpath(self):
        if os.path.isdir(self.capath):
            self.CERT_PATH = self.capath
        else:
            raise FileNotFoundError
    
    def create_ca(self):
        if not self.check_cafile(certifi.where()):
            raise FileNotFoundError
        customca = Path(self.CERT_PATH + '/customca.pem')
        with open(certifi.where(), 'r', encoding=ENCODING) as ca:
            ca_data = ca.read()
        with open(self.cafile, 'r', encoding=ENCODING) as ca:
            custom_ca_data = ca.read()
        # write out file
        ca_data += "\nISSUER: CN=Enteprise Cert\n"
        ca_data += custom_ca_data
        with open(customca, 'w', encoding=ENCODING) as ca:
            ca.write(ca_data)
        self.CUST_CA = str(customca)

    def check_cafiles(self, fn: str):
        if Path.exists(Path(fn)):
            return True
