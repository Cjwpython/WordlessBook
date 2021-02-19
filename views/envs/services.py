# coding: utf-8
import datetime
import uuid

from utils.db import envs_db, apps_db, namespaces_db
from utils.errors import EnvExist, NameSpaceExistEnv, EnvNotExist
from views.applications.services import delete_application


def create_env(data):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 创建一个应用
    env = {
        "_id": str(uuid.uuid4()),
        "name": data["name"],
        "nick_name": data["nick_name"],
        "namespace_id": data["namespace_id"],
        "create_time": now_time,
        "update_time": now_time,
        "apps": []
    }
    envs_db.envs.insert_one(env)
    namespace_add_env(namespace_id=data["namespace_id"], env_id=env["_id"])
    return env["_id"]


def namespace_add_env(namespace_id=None, env_id=None):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    namespaces_db.namespaces.update(
        {"_id": namespace_id},
        {
            "$addToSet": {"envs": env_id},
            "$set": {"update_time": now_time}}
    )


def check_namespce_exist_env(namespace_id, env_name, raise_exist=True):
    # 环境名称中是否存在这个命令空间
    envs = envs_db.envs.find({"name": env_name})
    for env in envs:
        if not env:  # 不存在说明这个环境刚创建
            return
        if namespace_id == env["namespace_id"] and raise_exist:
            # 存在的命名空间中，namespace_id 和新创建的环境的namespace_id 相同，说明命名空间下这个环境已经创建
            raise NameSpaceExistEnv


def check_namespce_exist_env_by_id(namespace_id, env_id, env_name):
    namespace = namespaces_db.namespaces.find_one({"_id": namespace_id})
    if env_id in namespace["envs"]:
        raise NameSpaceExistEnv
    for env_id in namespace["envs"]:
        env = envs_db.envs.find_one({"_id": env_id})
        if env["name"] == env_name:
            raise NameSpaceExistEnv


def check_env_exist_by_id(env_id, raise_exist=True):
    env = envs_db.envs.find_one({"_id": env_id})
    if env and raise_exist:
        raise EnvExist
    if not env and not raise_exist:
        raise EnvNotExist
    return env


def delete_env(env_id):
    env = envs_db.envs.find_one({"_id": env_id})  # 获取所有的应用
    for app_id in env["apps"]:
        delete_application(app_id)  # 删除所有的应用
    envs_db.envs.delete_one({"_id": env_id})


def update_env_namespace_id(env_id, namespace_id):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    envs_db.envs.update(
        {"_id": env_id},
        {
            "$set": {"update_time": now_time, "namespace_id": namespace_id}}
    )


def get_env_name(env_id):
    env = envs_db.envs.find_one({"_id": env_id})
    return env["name"]


def serialize_application_data(env):
    app_ids = env.pop("apps")
    env["apps"] = []
    for app_id in app_ids:
        app = apps_db.apps.find_one({"_id": app_id})
        env["apps"].append(app)
    return env
