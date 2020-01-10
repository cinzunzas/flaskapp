from datetime import datetime, timedelta

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from app.libs.crypto import Crypto
from app.libs.connection import Connection
import os, base64, json, hashlib, re, random, logging, inspect
from pprint import pprint

infologger = logging.getLogger('info')
debuglogger = logging.getLogger('debug')
errorlogger = logging.getLogger('error')
warninglogger = logging.getLogger('warning')


class SitesManager():
    # ToDo
    # Retorna el site segun code, ignorando si es mayuscula o minuscula
    def getByCode(self, code):
        return self.filter(name__iexact=code).first()

    # Retorna el public_key asociado al siteId sino retorna vacio
    def getPublicKey(self, siteId):
        return self.filter(id=siteId).first().public_key if (self.filter(id=siteId).first() is not None) else ''

    # Retorna arreglo de keys [public, private]
    def getKeys(self, siteId):
        public_key_filename = self.getPublicKey(siteId)
        public_key_path = os.path.join(settings.SECURITY_KEY_PATH, public_key_filename)
        if not os.path.isfile(public_key_path): return [None, None]

        with open(public_key_path, 'rb') as myfile:
            public_key = myfile.read()

        private_key_path = settings.SECURITY_PRIVATE_KEY
        if not os.path.isfile(private_key_path): return [None, None]

        with open(private_key_path, 'rb') as myfile:
            private_key = myfile.read()

        return [public_key, private_key]

    def encryptData(self, siteId, data, isBase64=True, mode="asymmetric"):
        (public_key, private_key) = self.getKeys(siteId)
        if public_key is None or private_key is None: return [None, None]

        encryptedData = signature = None
        if (mode == "asymmetric"):
            encryptedData = Crypto().encrypt(data, public_key, "public")
            signature = Crypto().sign(data, private_key)
        elif (mode == "symmetric"):
            (encryptedData, encryptedKey, signature) = Crypto().symmetricEncrypt(data, private_key, public_key)
            encryptedKey = base64.b64encode(encryptedKey).decode("utf-8")

        if isBase64 is True:
            encryptedData = base64.b64encode(encryptedData).decode("utf-8")
            signature = base64.b64encode(signature).decode("utf-8")

        # test decrypt
        # with open(os.path.join(settings.SECURITY_KEY_PATH, "groupon.prod.itier.cl.pem"), 'rb') as myfile: newprivate_key = myfile.read()
        # print(Crypto().decrypt(base64.b64decode(encryptedData), newprivate_key))
        if mode == "asymmetric":
            return [encryptedData, signature]
        elif mode == "symmetric":
            return [encryptedData, encryptedKey, signature]

        return True

    def decryptData(self, siteId, data, signature, isBase64=True, mode="asymmetric", key=""):
        (public_key, private_key) = self.getKeys(siteId)
        if public_key is None or private_key is None: return [None, None]

        decryptedData = ''

        if isBase64 is True:
            data = base64.b64decode(data)
            signature = base64.b64decode(signature)

        if mode == "asymmetric":
            privateKey = load_pem_private_key(private_key, password=None, backend=default_backend())
            decryptedData = privateKey.decrypt(
                data,
                padding.PKCS1v15()
            )
        elif mode == "symmetric":
            # desencriptar key
            key = base64.b64decode(key)
            decryptedData = Crypto().symmetricDecrypt(data, key, signature, private_key, public_key)

        return decryptedData

    def hookNotify(self, payment, finalStatus, multipart=False):
        failureReturnValue = "failed"
        successReturnValue = "confirmed"
        if finalStatus is "":
            # TODO: logear
            return failureReturnValue

        site = self.get(id=payment.site_id)

        if site is None or site.url_notify is None:
            # TODO: loggear
            return failureReturnValue

        data = {
            "order_number": str(payment.order_number),
            "amount": str(payment.amount),
            "status": str(payment.status),
            "notify": str(1)
        }

        # TODO: Loggear data notify

        postData = {}
        (postData["encdata"], postData["signature"]) = self.encryptData(payment.site_id, json.dumps(data))

        response = Connection().post(site.url_notify, postData, multipart)

        if response['code'] is not 200:
            return failureReturnValue

        return successReturnValue if response['body'] == "ok" else failureReturnValue
