# coding: utf-8
from apps import app
from .views import *

url_prefix = "/api/application"
app.add_url_rule(f"{url_prefix}s", view_func=get_all_applications, methods=['GET', ], strict_slashes=False)
app.add_url_rule(f"{url_prefix}/<application_id>", view_func=ApplicationConfigs.as_view("application_config"), methods=['GET', 'POST'], strict_slashes=False)
app.add_url_rule(f"{url_prefix}", view_func=Applications.as_view("application"), strict_slashes=False)
app.add_url_rule(f"{url_prefix}/change", view_func=application_change_env, methods=['POST', ], strict_slashes=False)
