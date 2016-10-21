import os
import binascii
import hashlib
from models import PrettySiteSettings, APIToken

class APIKey():

    def generateKey(self):
        return binascii.b2a_hex(os.urandom(15))

    def createMasterKey(self, k1, k2):
        m = hashlib.sha512()
        m.update(k1)
        m.update(k2)
        return m.hexdigest()

    def areTokensEnabledAndExist(self):
        tokensEnabled = PrettySiteSettings.getsettingvalue("API Tokens Enabled")
        if tokensEnabled == "True":
            tokenValue = APIToken.getAPItoken()
            if tokenValue:
                return True
        return False
