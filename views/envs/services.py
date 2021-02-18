# coding: utf-8
import datetime
import uuid

from utils.db import envs_db, namespaces_db
from utils.errors import EnvExist


def create_env(data):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 创建一个环境
    env = {
        "_id": str(uuid.uuid4()),
        "name": data["name"],
        "nick_name": data["nick_name"],
        "namespace_id": data["namespace_id"]
    }
    envs_db.envs.insert_one(env)
    # namespace中插入数据
    env_data = {
        env["_id"]: env
    }
    namespaces_db.namespaces.update({"_id": data["namespace_id"]}, {"$set": {"envs": env_data, "update_time": now_time}})
    return env["_id"]


def check_namespce_exist_env(namespace_id, env_name):
    # 环境名称中是否存在这个命令空间
    env = envs_db.envs.find_one({"name": env_name})
    if not env:  # 不存在说明这个环境刚创建
        return
    if namespace_id == env["namespace_id"]:
        # 存在的命名空间中，namespace_id 和新创建的环境的namespace_id 相同，说明命名空间下这个环境已经创建
        raise EnvExist
