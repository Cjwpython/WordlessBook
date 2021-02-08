# coding: utf-8
import json
from flask import request

from apps import app

import logging
logging.getLogger("request_handler")

# 设置请求钩子
@app.before_request
def before_request():
    if request.method.lower() == "get":
        if request.args:
            parameter = request.args.to_dict(flat=True)
            logging.info(f"requests parameter:\n {parameter}")
    else:
        try:
            request_data = json.loads(str(request.data, encoding="utf-8"))
            logging.info(f"requests data : \n{request_data}")
        except Exception as e:
            logging.info(e)


@app.after_request
def after_request(request):
    return_data = None
    try:
        return_data = json.loads(str(request.data, encoding="utf-8"))
    except Exception as e:
        logging.info(e)
    if return_data:
        if request.status_code // 200 > 1:
            logging.error(f"return data : \n{return_data}")
        else:
            logging.info(f"return data : \n{return_data}")
    return request
