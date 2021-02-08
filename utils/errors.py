# coding: utf-8
from utils.base_error import BaseError


class ParameterError(BaseError):
    error_id = "PARAMETER_ERROR"
    error_message = "请求参数不符合要求"
    status_code = 400

    def __init__(self, error_msg=None):
        if error_msg:
            self.error_message = error_msg