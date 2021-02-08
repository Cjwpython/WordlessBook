# coding: utf-8
from flask import jsonify
from apps import app
from utils.base_error import BaseError, handle_api_exception, handle_internal_exception

import logging

logging.getLogger("errorhandler")


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"code": 404, "message": f"{e.description}"}), 404


@app.errorhandler(405)
def method_not_allow(e):
    return jsonify({"code": 405, "message": f"{e.description}"}), 405


@app.errorhandler(500)
def method_not_allow(e):
    logging.error(e)
    return jsonify({"code": 500, "message": "Some Bad Thing Happen"}), 500


@app.errorhandler(401)
def verification_failed(e):
    return jsonify({"code": 401, "message": "Identity Verification Failed"}), 401


app.register_error_handler(BaseError, handle_api_exception)
app.register_error_handler(Exception, handle_internal_exception)
