# coding: utf-8
from utils.base_error import BaseError


class ParameterError(BaseError):
    error_id = "PARAMETER_ERROR"
    error_message = "请求参数不符合要求"
    status_code = 400

    def __init__(self, error_msg=None):
        if error_msg:
            self.error_message = error_msg


class NamespaceExist(BaseError):
    error_id = "NAMESPACE_ERROR"
    error_message = "命名空间已存在"
    status_code = 400

    def __init__(self, error_msg=None):
        if error_msg:
            self.error_msg = error_msg


class NamespaceNotExist(BaseError):
    error_id = "NAMESPACE_ERROR"
    error_message = "命名空间未创建"
    status_code = 400

    def __init__(self, error_msg=None):
        if error_msg:
            self.error_msg = error_msg


class NameSpaceExistEnv(BaseError):
    error_id = "ENV_ERROR"
    error_message = "命名空间下已存在该环境"
    status_code = 400

    def __init__(self, error_msg=None):
        if error_msg:
            self.error_msg = error_msg


class EnvExist(BaseError):
    error_id = "ENV_ERROR"
    error_message = "环境已经存在"
    status_code = 400

    def __init__(self, error_msg=None):
        if error_msg:
            self.error_msg = error_msg


class EnvNotExist(BaseError):
    error_id = "ENV_ERROR"
    error_message = "环境不存在"
    status_code = 400

    def __init__(self, error_msg=None):
        if error_msg:
            self.error_msg = error_msg
