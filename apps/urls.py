# coding: utf-8

def register_url(app):
    """
    URL总路由  每个视图独立注册路由
    :param app:
    :return:
    """
    from views.test import urls  # 注册测试视图的路由
    from views.namespaces import urls  # 注册命名空间视图的路由
    from views.envs import urls  # 注册环境视图的路由
