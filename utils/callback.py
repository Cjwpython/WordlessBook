# coding: utf-8

from flask import jsonify


def success_msg(message="", code=200):
    return jsonify({"code": code, "message": message}), code


def fail_msg(message="", code=400):
    return jsonify({"code": code, "message": message}), 400
