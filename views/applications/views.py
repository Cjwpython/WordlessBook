# coding: utf-8
import uuid
from pprint import pprint

from flask import jsonify, views, request

from middleware.validate import check_date
from utils.db import envs_db, apps_db
import logging

from views.applications.services import create_application, check_env_exist_application, check_application_exist_by_id, env_delete_application, update_application_env_id, env_add_application, check_env_exist_application_by_id, \
    update_application_configs
from views.applications.validate import create_app_validate, update_application_validate, delete_application_validate, application_change_env_validate, create_config_validate
from views.envs.services import check_namespce_exist_env, check_env_exist_by_id, get_env_name
from views.namespaces.services import check_namespaces_exist_by_id

logging.getLogger("test.views")


def get_all_applications():
    params = request.args.to_dict(flat=True)
    pagiation = int(params.get("pagiation", 1))
    env_id = params.get("env_id", None)
    data = {}
    data["apps"] = []
    current_page = params.get("current_page", 1)
    current_max_row = params.get("current_max_row", 15)
    sort_type = params.get("sort_type", "update_time")
    skip = (int(current_page) - 1) * int(current_max_row)
    if sort_type not in ["create_time", "update_time"]:
        sort_type = "update_time"
    if env_id:
        check_env_exist_by_id(env_id=env_id, raise_exist=False)
        max_count = apps_db.apps.find({"env_id": env_id}).count()
        apps = apps_db.apps.find({"env_id": env_id}, {"name": 1, "nick_name": 1, "env_id": 1}).sort(sort_type, -1).skip(int(skip)).limit(int(current_max_row))  # 只返回名称和昵称
    else:
        max_count = apps_db.apps.find({}).count()
        apps = apps_db.apps.find({}, {"name": 1, "nick_name": 1, "env_id": 1}).sort(sort_type, -1).skip(int(skip)).limit(int(current_max_row))  # 只返回名称和昵称
    if not pagiation:
        apps = apps_db.apps.find({}, {"name": 1, "nick_name": 1, "env_id": 1}).sort(sort_type, -1)  # 只返回名称和昵称
        if env_id:
            apps = apps_db.apps.find({"env_id": env_id}, {"name": 1, "nick_name": 1, "env_id": 1}).sort(sort_type, -1)  # 只返回名称和昵称
    for app in apps:
        env_name = get_env_name(env_id=app["env_id"])
        app["env_name"] = env_name
        data["apps"].append(app)
    if pagiation:
        data["max_count"] = max_count
        data["current_page"] = current_page
        data["current_max_row"] = current_max_row
        data["sort_type"] = sort_type
    return jsonify({"data": data, "status_code": 200}), 200


class ApplicationConfigs(views.MethodView):
    def get(self, application_id):
        application = check_application_exist_by_id(application_id=application_id, raise_exist=False)
        env_name = get_env_name(env_id=application["env_id"])
        application["env_name"] = env_name
        return jsonify({"data": application, "status_code": 200}), 200

    @check_date(schema=create_config_validate)
    def post(self, application_id):
        check_application_exist_by_id(application_id=application_id, raise_exist=False)
        data = request.json
        configs = data["configs"]
        update_application_configs(application_id=application_id, configs=configs)
        return jsonify({"message": "配置已生效", "status_code": 200}), 200


class Applications(views.MethodView):
    @check_date(schema=create_app_validate)
    def post(self):
        data = request.json
        check_env_exist_by_id(env_id=data["env_id"], raise_exist=False)
        check_env_exist_application(env_id=data["env_id"], application_name=data["name"])
        env_id = create_application(data)
        return jsonify({"code": 201, "message": f"{env_id}创建成功"}), 201

    @check_date(schema=update_application_validate)
    def put(self):
        data = request.json
        application_id = data["application_id"]
        nick_name = data["nick_name"]
        check_application_exist_by_id(application_id=application_id, raise_exist=False)
        apps_db.apps.update({"_id": application_id}, {"$set": {"nick_name": nick_name}})
        return jsonify({"code": 200, "message": "更新成功"}), 200

    @check_date(schema=delete_application_validate)
    def delete(self):
        data = request.json
        application_id = data["application_id"]
        application = check_application_exist_by_id(application_id=application_id, raise_exist=False)
        apps_db.apps.delete_one({"_id": application_id})
        # 环境删除应用
        env_delete_application(env_id=application["env_id"], application_id=application_id)
        return jsonify({"code": 200, "message": "删除成功"}), 200


@check_date(schema=application_change_env_validate)
def application_change_env():
    data = request.json
    env_id = data["env_id"]
    application_id = data["application_id"]
    current_env_id = data["current_env_id"]
    check_env_exist_by_id(env_id=env_id, raise_exist=False)
    check_env_exist_by_id(env_id=current_env_id, raise_exist=False)
    application = check_application_exist_by_id(application_id=application_id, raise_exist=False)
    check_env_exist_application_by_id(env_id=env_id, application_id=application_id,application_name=application["name"])
    env_delete_application(env_id=current_env_id, application_id=application_id)
    update_application_env_id(application_id=application_id, env_id=env_id)
    env_add_application(env_id=env_id, application_id=application_id)
    return jsonify({"code": 200, "message": "修改成功"}), 200
