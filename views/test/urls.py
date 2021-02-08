# coding: utf-8
from apps import app
from .views import *

url_prefix = "/abc/123"
app.add_url_rule("/index", view_func=index1, methods=['GET', ], strict_slashes=False)
app.add_url_rule("/app", view_func=Task.as_view("apps"), strict_slashes=False)
