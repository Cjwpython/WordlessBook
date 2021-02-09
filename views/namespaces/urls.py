# coding: utf-8
from apps import app
from .views import *

url_prefix = "/api/namespaces"
app.add_url_rule(f"{url_prefix}", view_func=get_list_namespaces, methods=['GET', ], strict_slashes=False)
app.add_url_rule("/api/namespace/<namespace_id>", view_func=get_single_namespace, methods=['GET', ], strict_slashes=False)
app.add_url_rule("/api/namespace", view_func=Namespace.as_view("namespace"), strict_slashes=False)
