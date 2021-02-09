# coding: utf-8
from apps import app
from .views import *

url_prefix = "/api/env"
app.add_url_rule(f"{url_prefix}s", view_func=get_all_envs, methods=['GET', ], strict_slashes=False)
app.add_url_rule(f"{url_prefix}/<env_id>", view_func=get_single_env, methods=['GET', ], strict_slashes=False)
app.add_url_rule(f"{url_prefix}", view_func=Env.as_view("env"), strict_slashes=False)
