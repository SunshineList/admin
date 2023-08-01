# -*- coding: utf-8 -*-
import base64
import os
import random
import re
import string

from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from rest_framework import exceptions

key_str = """MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAKh8g7a3RS+mi89p
xxh1JtW1q+e+mwYJMQia+rPqMVLb4vCKGl5bxXCUroG3pUUCcSDKoBruvsj9bMVY
J/6Tg3xKNJGZevBwXRRULbtutE+KGRgWdvgPn3CVa4YMd2sNLnxqlYk0aXEpXwhv
SXdUbloUIdstp6I7rwVAHb3o/7+jAgMBAAECfyDoMNF++gRUgvn/ruMX/n2+/dRF
ZgHHycvkeRKqqveD+s8AKiZDxkw2vd6X/696yp2c9ahM+PZIiPYCQc13AjbzI88/
OvznFHxfLovtd/6Wcm2Y6Owdh9U4svaW4o9l7mUQ9wVXl7jVa6PZDhlXF4jGNohT
ZpX77MYEW0+ruRECQQDTU4AXE+SHuOx5kf5aWcMfw7SSPAUuwjIf7wPDp/NzrLUw
K9JnqxWspZFkx1qffcIikDHYGSZR/S2Lo3fJwD0/AkEAzBqe43pS6Esga6uEMv7J
kQiCAn/33ouWxK7DXhFC8yatpBdZEUhE0wj1qsoQcWb/B1fFS6iJTXrDhbsnQunQ
nQJASNu6BrraCJ0OEp/uBLJ73oC3yc8drlBPvcjHEHbgLZp24YPKR+mpUFvI8+jz
apeODiKOvMV2+7+BK2qRiyJXOwJBAJbmE5SxCnzNlmGkRDADqXi95oj8nYB+iXBO
mQiCEJJ+hSBtVp9tY9z2odKsY+3DrUd7f9WI/EI5QjcsAEH7Zg0CQQCVpy6IPNfq
usqbZDxFcxMJSVRtvqBxBFpn/vvHVyCcaL6tFp1TW1dRAA1NQptRSjdd5+IN2M7U
Ki3VkKr2LGf/"""

PRIVATE_KEY = '-----BEGIN PRIVATE KEY-----\n' + key_str + '\n-----END PRIVATE KEY-----'


def random_valid_code(length=4):
    """
    随机验证码
    :param length:
    :return:
    """
    num_letter = string.ascii_letters + string.digits
    num_letter = re.sub('[BLOZSloz81025]', '', num_letter)
    return ''.join(random.sample(num_letter, length))


def decrypt_pass(password):
    random_generator = Random.new().read
    RSA.generate(1024, random_generator)
    rsakey = RSA.importKey(PRIVATE_KEY)
    cipher = PKCS1_v1_5.new(rsakey)
    try:
        return cipher.decrypt(base64.b64decode(password), random_generator)
    except Exception as e:
        raise exceptions.ValidationError('密码错误')
