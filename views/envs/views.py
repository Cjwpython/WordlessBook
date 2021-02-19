# coding: utf-8
import uuid
from pprint import pprint

from flask import jsonify, views, request

from middleware.validate import check_date
from utils.db import envs_db
import logging

from views.envs.services import check_namespce_exist_env, check_env_exist_by_id, create_env, update_env_namespace_id, namespace_add_new_env
from views.envs.validate import create_env_validate, update_env_validate, delete_env_validate, change_env_namespace_validate
from views.namespaces.services import check_namespaces_exist_by_id, get_namespace_name, namespace_delete_env

logging.getLogger("test.views")


def get_all_envs():
    params = request.args.to_dict(flat=True)
    namespace_id = params.get("namespace_id", None)
    data = {}
    data["envs"] = []
    current_page = params.get("current_page", 1)
    current_max_row = params.get("current_max_row", 15)
    sort_type = params.get("sort_type", "update_time")
    skip = (int(current_page) - 1) * int(current_max_row)
    if sort_type not in ["create_time", "update_time"]:
        sort_type = "update_time"
    if namespace_id:
        check_namespaces_exist_by_id(id=namespace_id, raise_exist=False)
        max_count = envs_db.envs.find({"namespace_id": namespace_id}).count()
        envs = envs_db.envs.find({"namespace_id": namespace_id}, {"name": 1, "nick_name": 1, "namespace_id": 1}).sort(sort_type, -1).skip(int(skip)).limit(int(current_max_row))  # 只返回名称和昵称
    else:
        max_count = envs_db.envs.find({}).count()
        envs = envs_db.envs.find({}, {"name": 1, "nick_name": 1, "namespace_id": 1}).sort(sort_type, -1).skip(int(skip)).limit(int(current_max_row))  # 只返回名称和昵称
    for env in envs:
        print(env)
        namespace_name = get_namespace_name(namespace_id=env["namespace_id"])
        env["namespace_name"] = namespace_name
        data["envs"].append(env)
    data["max_count"] = max_count
    data["current_page"] = current_page
    data["current_max_row"] = current_max_row
    data["sort_type"] = sort_type
    return jsonify({"data": data}), 200


def get_single_env(env_id):
    env = check_env_exist_by_id(env_id=env_id, raise_exist=False)
    namespace_name = get_namespace_name(namespace_id=env["namespace_id"])
    env["namespace_name"] = namespace_name
    return jsonify({"data": env}), 200


class Env(views.MethodView):
    @check_date(schema=create_env_validate)
    def post(self):
        data = request.json
        check_namespaces_exist_by_id(id=data["namespace_id"], raise_exist=False)
        check_namespce_exist_env(namespace_id=data["namespace_id"], env_name=data["name"])
        env_id = create_env(data)
        return jsonify({"code": 201, "message": f"{env_id}创建成功"}), 201

    @check_date(schema=update_env_validate)
    def put(self):
        data = request.json
        env_id = data["env_id"]
        nick_name = data["nick_name"]
        check_env_exist_by_id(env_id=env_id, raise_exist=False)
        envs_db.envs.update({"_id": env_id}, {"$set": {"nick_name": nick_name}})
        return jsonify({"code": 200, "message": "更新成功"}), 200

    @check_date(schema=delete_env_validate)
    def delete(self):
        data = request.json
        env_id = data["env_id"]
        env = check_env_exist_by_id(env_id=env_id, raise_exist=False)
        envs_db.envs.delete_one({"_id": env_id})
        # 命名空间删除环境
        namespace_delete_env(namespace_id=env["namespace_id"], env_id=env_id)
        return jsonify({"code": 200, "message": "删除成功"}), 200


@check_date(schema=change_env_namespace_validate)
def env_change_namespcae():
    data = request.json
    env_id = data["env_id"]
    namespace_id = data["namespace_id"]
    current_namespace_id = data["current_namespace_id"]
    check_namespaces_exist_by_id(id=namespace_id, raise_exist=False)
    check_namespaces_exist_by_id(id=current_namespace_id, raise_exist=False)
    check_env_exist_by_id(env_id=env_id, raise_exist=False)
    env = envs_db.envs.find_one({"_id": env_id})
    env_name = env["name"]
    check_namespce_exist_env(namespace_id=namespace_id, env_name=env_name)
    namespace_delete_env(namespace_id=current_namespace_id, env_id=env_id)
    update_env_namespace_id(env_id, namespace_id=namespace_id)
    namespace_add_new_env(namespace_id=namespace_id, env_id=env_id)
    return jsonify({"code": 200, "message": "修改成功"}), 200
