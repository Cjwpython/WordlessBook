# coding: utf-8
from apps import app
from apps.urls import register_url

register_url(app)  # 注册路由，这里是总路由



from middleware.errorhandler import *  # 调用异常捕获类
from middleware.request_handler import *  # 调用请求钩子
app.app_context().push()  # 推送上下文之后，下方中间层才能使用current_app