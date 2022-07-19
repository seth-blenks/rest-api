from uuid import uuid4
from datetime import datetime
import hashlib
from flask import current_app
from hmac import HMAC



def gen_api_keys():
    key_token = uuid4().hex + str(datetime.now().timestamp).replace('.', '')
    public_key = HMAC(current_app.config['SECRET_KEY'].encode('utf8'), key_token.encode('utf8'), digestmod = hashlib.sha256)

    private_token = 'private' + uuid4().hex + str(datetime.now().timestamp).replace('.', '')
    private_key = HMAC(current_app.config['SECRET_KEY'].encode('utf8'), private_token.encode('utf8'), digestmod = hashlib.sha256)

    return (public_key.hexdigest(), private_key.hexdigest())
