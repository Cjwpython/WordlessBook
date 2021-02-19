# coding: utf-8
import uuid
from pprint import pprint

from flask import jsonify, views, request

from middleware.validate import check_date
from utils.db import envs_db, apps_db
import logging

from views.applications.services import create_application, check_env_exist_application, check_application_exist_by_id, env_delete_application
from views.applications.validate import create_app_validate, update_application_validate
from views.envs.services import check_namespce_exist_env, check_env_exist_by_id, get_env_name
from views.namespaces.services import check_namespaces_exist_by_id, get_namespace_name

logging.getLogger("test.views")


# def get_all_applications():
#     params = request.args.to_dict(flat=True)
#     pagiation = int(params.get("pagiation", 1))
#     namespace_id = params.get("namespace_id", None)
#     data = {}
#     data["apps"] = []
#     current_page = params.get("current_page", 1)
#     current_max_row = params.get("current_max_row", 15)
#     sort_type = params.get("sort_type", "update_time")
#     skip = (int(current_page) - 1) * int(current_max_row)
#     if sort_type not in ["create_time", "update_time"]:
#         sort_type = "update_time"
#     if namespace_id:
#         check_namespaces_exist_by_id(id=namespace_id, raise_exist=False)
#         max_count = envs_db.envs.find({"namespace_id": namespace_id}).count()
#         envs = envs_db.envs.find({"namespace_id": namespace_id}, {"name": 1, "nick_name": 1, "namespace_id": 1}).sort(sort_type, -1).skip(int(skip)).limit(int(current_max_row))  # 只返回名称和昵称
#     else:
#         max_count = envs_db.envs.find({}).count()
#         envs = envs_db.envs.find({}, {"name": 1, "nick_name": 1, "namespace_id": 1}).sort(sort_type, -1).skip(int(skip)).limit(int(current_max_row))  # 只返回名称和昵称
#     for env in envs:
#         print(env)
#         namespace_name = get_namespace_name(namespace_id=env["namespace_id"])
#         env["namespace_name"] = namespace_name
#         data["envs"].append(env)
#     data["max_count"] = max_count
#     data["current_page"] = current_page
#     data["current_max_row"] = current_max_row
#     data["sort_type"] = sort_type
#     return jsonify({"data": data}), 200

#
def get_single_applications(application_id):
    application = check_application_exist_by_id(application_id=application_id, raise_exist=False)
    env_name = get_env_name(env_id=application["env_id"])
    application["namespace_name"] = env_name
    return jsonify({"data": application}), 200


class Applications(views.MethodView):
    @check_date(schema=create_app_validate)
    def post(self):
        data = request.json
        check_namespaces_exist_by_id(id=data["namespace_id"], raise_exist=False)
        check_env_exist_by_id(env_id=data["env_id"], raise_exist=False)
        env = envs_db.envs.find_one({"_id": data["env_id"]})
        check_namespce_exist_env(namespace_id=data["namespace_id"], env_name=env["name"], raise_exist=False)
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

    def delete(self):
        data = request.json
        application_id = data["application_id"]
        application = check_application_exist_by_id(application_id=application_id, raise_exist=False)
        apps_db.apps.delete_one({"_id": application_id})
        # 环境删除应用
        env_delete_application(env_id=application["env_id"], application_id=application_id)
