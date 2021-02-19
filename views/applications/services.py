# coding: utf-8
import datetime
import uuid

from utils.db import envs_db, namespaces_db, apps_db
from utils.errors import EnvExist, NameSpaceExistEnv, EnvNotExist


def create_application(data):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 创建一个环境
    app = {
        "_id": str(uuid.uuid4()),
        "name": data["name"],
        "nick_name": data["nick_name"],
        "namespace_id": data["namespace_id"],
        "env_id": data["env_id"],
        "create_time": now_time,
        "update_time": now_time,
    }
    apps_db.apps.insert_one(app)
    # env中插入数据
    env_add_application(env_id=data["env_id"], application_id=data["_id"])
    return app["_id"]


def env_add_application(env_id=None, application_id=None):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    envs_db.envs.update(
        {"_id": env_id},
        {
            "$addToSet": {"envs": application_id},
            "$set": {"update_time": now_time}}
    )


def check_namespce_exist_env(namespace_id, env_name):
    # 环境名称中是否存在这个命令空间
    env = envs_db.envs.find_one({"name": env_name})
    if not env:  # 不存在说明这个环境刚创建
        return
    if namespace_id == env["namespace_id"]:
        # 存在的命名空间中，namespace_id 和新创建的环境的namespace_id 相同，说明命名空间下这个环境已经创建
        raise NameSpaceExistEnv


def check_env_exist_by_id(env_id, raise_exist=True):
    env = envs_db.envs.find_one({"_id": env_id})
    if env and raise_exist:
        raise EnvExist
    if not env and not raise_exist:
        raise EnvNotExist
