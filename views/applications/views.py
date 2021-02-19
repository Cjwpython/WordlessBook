# coding: utf-8
import uuid
from pprint import pprint

from flask import jsonify, views, request

from middleware.validate import check_date
from utils.db import envs_db
import logging

from views.applications.validate import create_app_validate
from views.envs.services import check_namespce_exist_env, check_env_exist_by_id, create_app
from views.namespaces.services import check_namespaces_exist_by_id, get_namespace_name

logging.getLogger("test.views")


# def get_all_applications():
#     data = []
#     envs = envs_db.envs.find({}, {"name": 1, "nick_name": 1})  # 只返回名称和昵称
#     for env in envs:
#         data.append(env)
#     return jsonify({"data": data}), 200
#
#
# def get_single_applications(application_id):
#     check_env_exist_by_id(env_id=env_id, raise_exist=False)
#     env = envs_db.envs.find_one({"_id": env_id})
#     namespace_name = get_namespace_name(namespace_id=env["namespace_id"])
#     env["namespace_name"] = namespace_name
#     return jsonify({"data": env}), 200


class Applications(views.MethodView):
    @check_date(schema=create_app_validate)
    def post(self):
        data = request.json
        # 判断命名空间存在性
        check_namespaces_exist_by_id(id=data["namespace_id"], raise_exist=False)
        # 判断环境存在性
        check_env_exist_by_id(env_id=data["env_id"], raise_exist=False)
        # 判断环境和命令空间的关联性
        env = envs_db.envs.find_one({"_id": data["env_id"]})
        check_namespce_exist_env(namespace_id=data["namespace_id"], env_name=env["name"])
        env_id = create_app(data)
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