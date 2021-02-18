# coding: utf-8
import uuid
from pprint import pprint

from flask import jsonify, views, request

from middleware.validate import check_date
from utils.db import envs_db
import logging

from views.envs.services import create_env, check_namespce_exist_env, check_env_exist_by_id
from views.envs.validate import create_env_validate
from views.namespaces.services import check_namespaces_exist_by_id, get_namespace_name

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
        max_count = envs_db.envs.find({"namespace_id": namespace_id}).count()
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
    check_env_exist_by_id(env_id=env_id, raise_exist=False)
    env = envs_db.envs.find_one({"_id": env_id})
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

    def put(self):
        env_id = request.json.get("env_id")
        name = request.json.get("name")
        nick_name = request.json.get("nick_name")
        check_env_exist_by_id(env_id=env_id, raise_exist=False)
        env = envs_db.envs.find_one({"_id": env_id})
        if not env:
            return jsonify({"code": 400, "message": "环境不存在"}), 400
        envs_db.envs.update({"_id": env_id}, {"name": name, "nick_name": nick_name})
        return jsonify({"code": 200, "message": "更新成功"}), 200

    def delete(self):
        env_id = request.json.get("env_id")
        env = envs_db.envs.find_one({"_id": envs_db})
        if not env:
            return jsonify({"code": 400, "message": "环境不存在"}), 400
        envs_db.envs.delete_one({"_id": env_id})
        return jsonify({"code": 200, "message": "删除成功"}), 200
