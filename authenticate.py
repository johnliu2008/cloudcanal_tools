import hashlib
import hmac
import urllib.parse
import base64
import random
import string

import config


def compose_string_to_sign(queries):
    sorted_keys = sorted(queries.keys())
    query_string = "&".join(
        "{}={}".format(percent_encode(key), percent_encode(queries[key]))
        for key in sorted_keys
    )
    return percent_encode(query_string)


def percent_encode(value):
    return urllib.parse.quote(value, safe='~')


def sign_string(string_to_sign, access_key_secret):
    hmac_obj = hmac.new(access_key_secret.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha1)
    signature = base64.b64encode(hmac_obj.digest()).decode('utf-8')
    return signature


def generate_public_params():
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    param_to_sign = {
        "SignatureMethod": "HMAC-SHA1",
        "SignatureNonce": ran_str,
        "AccessKeyId": config.CC_AccessKeyId
    }
    param_str = compose_string_to_sign(param_to_sign)
    signature = sign_string(param_str, config.CC_secret_key)
    public_params = param_str + '&Signature=%s' % (signature)
    # public_params = percent_encode(param_str + '&Signature=%s' % (signature))
    # print(public_params)
    return public_params


def quoted_public_params():
    """返回转换成URL编码格式后的签名串"""
    public_params = generate_public_params()
    return urllib.parse.quote(public_params, safe='~')


def unquoted_public_params():
    """返回未被转换成URL编码格式的签名串"""
    public_params = generate_public_params()
    return urllib.parse.unquote(public_params)


# generate_public_params()
# print(quoted_public_params())
# print(unquoted_public_params())
