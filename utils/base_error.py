# coding: utf-8
from flask import jsonify
import logging
logging.getLogger("base_error")

class BaseError(Exception):
    error_id = "BASE_ERROR"
    error_message = ""
    status_code = 500

    def __str__(self):
        return "<{err_id}>: <{status_code}>: <{err_msg}>".format(
            err_id=self.error_id,
            status_code=self.status_code,
            err_msg=self.error_message,
        )

    def render(self):
        return {
            "status_code": self.status_code,
            "error_id": self.error_id,
            "message": self.error_message,
        }


def handle_api_exception(error):
    rsp = error.render()
    logging.exception(error)
    return jsonify(rsp), error.status_code


def handle_internal_exception(error):
    logging.exception(error)
    return jsonify({"error_id": "INTERNAL_ERROR", "message": str(error), "status_code": 500}), 500
