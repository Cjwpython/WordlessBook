# coding: utf-8
from functools import wraps

from flask import request
from jsonschema import ValidationError, validate

from utils.errors import ParameterError


def check_date(schema):
    """
    校验非get的所有请求的参数
    TODO 添加get 请求的参数校验(规避所有的非法参数)
    :param schema: jsonschema 规定的参数格式 必传
    :return:
    """

    def inner_decorator(func):
        @wraps(func)
        def wrapper_func(*args, **kwargs):
            try:
                data = request.json
                validate(instance=data, schema=schema)
            except ValidationError as e:
                raise ParameterError(e.message)  # 重新定义错误返回格式
            ret = func(*args, **kwargs)
            return ret

        return wrapper_func

    return inner_decorator
