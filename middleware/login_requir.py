# coding: utf-8
import json
from functools import wraps
from flask import current_app, abort
from flask import request

import logging
logging.getLogger("login_requir")

def verify_key(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            if request.method.lower() == "get":
                parameter = request.args.to_dict(flat=True)
                if parameter["key"] != current_app.config["SECERT_KEY"]:
                    abort(401)
            else:
                request_data = json.loads(str(request.data, encoding="utf-8"))
                if request_data["key"] != current_app.config["SECERT_KEY"]:
                    abort(401)
        except Exception as e:
            logging.error(e)
            abort(401)
        return func(*args, **kwargs)

    return inner
