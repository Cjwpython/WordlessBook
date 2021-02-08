# coding: utf-8
from flask import jsonify, views
import time
from utils.errors import ParameterError
import logging
logging.getLogger("test.views")


# @verify_key
def index1():
    for i in range(1000):
        logging.debug(i)
        time.sleep(1)
    return jsonify({"code": 200})


class Task(views.MethodView):

    def get(self):
        logging.debug("get url >> app")
        return jsonify({"code": 2000})

    def post(self):
        return jsonify({"code": 200})
