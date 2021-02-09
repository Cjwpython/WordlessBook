# coding: utf-8
import uuid
from pprint import pprint

from flask import jsonify, views, request

from utils.db import envs_db
import logging

logging.getLogger("test.views")


def get_all_envs():
    data = []
    envs = envs_db.envs.find({}, {"name": 1, "nick_name": 1})  # 只返回名称和昵称
    for env in envs:
        data.append(env)
    return jsonify({"data": data}), 200


def get_single_env(env_id):
    data = []
    env = envs_db.envs.find_one({"_id": env_id})
    if env:
        data.append(env)
    return jsonify({"data": data}), 200


class Env(views.MethodView):

    def post(self):
        env = {
            "_id": str(uuid.uuid4()),
            "name": request.json.get("name"),
            "nick_name": request.json.get("nick_name")
        }
        envs_db.envs.insert_one(env)
        return jsonify({"code": 201, "message": "创建成功"}), 201

    def put(self):
        env_id = request.json.get("env_id")
        name = request.json.get("name")
        nick_name = request.json.get("nick_name")
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
