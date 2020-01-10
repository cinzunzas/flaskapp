# -*- coding: utf-8 -*-
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa, rsa, padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from Crypto.Cipher import AES
import os, random, string, chardet, pprp, base64


class Crypto:
    def encrypt(self, data, key, typeKey="public"):
        if key is None:
            # loggear
            return False;
        retorno = None
        if typeKey == "public":
            key = load_pem_public_key(key, backend=default_backend())
            # isinstance(key, rsa.RSAPublicKey)
            serialized_public = key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            retorno = key.encrypt(
                bytes(data, 'utf-8'),
                padding.PKCS1v15()
            )
        elif typeKey == "private":
            key = load_pem_private_key(key, None, backend=default_backend())
            # isinstance(key, rsa.RSAPublicKey)
            serialized_public = key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8
            )
            retorno = key.encrypt(
                data if (isinstance(data, (bytes, bytearray))) else bytes(data, 'utf-8'),
                padding.PKCS1v15()
            )
        if retorno is None:
            # Loggear
            return False
        return retorno

    def sign(self, data, key):
        if data is None or key is None:
            # loggear
            return False
        privateKey = load_pem_private_key(key, None, default_backend())
        signature = privateKey.sign(
            data if (isinstance(data, (bytes, bytearray))) else bytes(data, 'utf-8'),
            padding.PKCS1v15(),
            hashes.SHA1()
        )

        if signature is None:
            # Loggear
            return False

        return signature

    def decrypt(self, data, key, typeKey="private"):
        if key is None or data is None:
            # loggear
            return False;

        decryptedData = ''
        if typeKey == "private":
            privateKey = serialization.load_pem_private_key(key, password=None, backend=default_backend())
            decryptedData = privateKey.decrypt(
                data,
                padding.PKCS1v15()
            )
        if decryptedData == '':
            # loggear
            return False
        return decryptedData

    def verify(self, data, signature, key):
        if data is None or key is None or signature is None:
            # loggear
            return False

        try:
            public_key = load_pem_public_key(key, backend=default_backend())
            verify = public_key.verify(
                signature,
                data if (isinstance(data, (bytes, bytearray))) else bytes(data, 'utf-8'),
                padding.PKCS1v15(),
                hashes.SHA1()
            )
        except InvalidSignature as e:
            # loggear invalidasignature
            return False
        except Exception as e:
            # loggear
            return False

        return True

    # Conversion basada en https://stackoverflow.com/questions/8217269/decrypting-strings-in-python-that-were-encrypted-with-mcrypt-rijndael-256-in-php/45653735#45653735
    def decryptRjindael(self, key, data):

        key_size = 16
        block_size = 32
        padded_key = key.ljust(key_size, b'\0')

        ciphertext = base64.b64decode(data)

        sg = pprp.data_source_gen(ciphertext, block_size=block_size)
        dg = pprp.rjindael_decrypt_gen(padded_key, sg, block_size=block_size)

        return pprp.decrypt_sink(dg).decode('utf-8')

    def symmetricEncrypt(self, data, private_key, public_key):
        encryptionKey = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))

        # Encriptar data con encryptionKey
        cipher = AES.new(encryptionKey)
        # AES.key_size = 128
        encryptedData = cipher.encrypt(data)
        if encryptedData is None:
            # Loggear
            return False
        # Encriptar key
        encryptedKey = self.encrypt(encryptionKey, public_key)
        signature = self.sign(encryptedKey, private_key)

        return [encryptedData, encryptedKey, signature]

    def symmetricDecrypt(self, data, encryptedKey, signature, private_key, public_key):
        decryptedKey = self.decrypt(encryptedKey, private_key)

        # Verificar con firma y public_key
        if self.verify(decryptedKey, signature, public_key) is not True:
            # loggear
            return False

        decryptedData = self.decryptRjindael(decryptedKey, data)

        if decryptedData != "":
            return decryptedData

        return True
