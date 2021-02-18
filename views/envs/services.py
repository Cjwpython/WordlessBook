# coding: utf-8
import uuid

from flask import jsonify

from utils.db import envs_db, namespaces_db


def create_env(data):
    env = {
        "_id": str(uuid.uuid4()),
        "name": data["name"],
        "nick_name": data["nick_name"]
    }
    envs_db.envs.insert_one(env)
    return env["_id"]


def check_namespaces_exist(name):
    namespace = namespaces_db.namespaces.find_one({"name": name})
    if not namespace:
        return jsonify({"status_code": 400, "message": f"{name}命令空间未创建"}), 400
