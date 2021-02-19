# coding: utf-8
import uuid
import datetime

from utils.db import namespaces_db, envs_db
from utils.errors import NamespaceExist, NamespaceNotExist
from views.envs.services import delete_env


def create_namespace(data):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    namespace = {
        "_id": str(uuid.uuid4()),
        "name": data["name"],
        "nick_name": data["nick_name"],
        "create_time": now_time,
        "update_time": now_time,
        "envs": []
    }

    namespaces_db.namespaces.insert_one(namespace)
    return namespace["_id"]


def check_namespaces_exist_by_name(name, raise_exist=False):
    namespace = namespaces_db.namespaces.find_one({"name": name})
    if namespace and raise_exist:
        raise NamespaceExist
    if not namespace and raise_exist:
        return NamespaceNotExist


def check_namespaces_exist_by_id(id, raise_exist=True):
    namespace = namespaces_db.namespaces.find_one({"_id": id})
    if namespace and raise_exist:
        raise NamespaceExist
    if not namespace and not raise_exist:
        raise NamespaceNotExist


def update_namespace(data):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    namespace_id = data["namespace_id"]
    nick_name = data["nick_name"]
    namespaces_db.namespaces.update({"_id": namespace_id}, {"$set": {"nick_name": nick_name, "update_time": now_time}}, upsert=True)


def delete_namespace(data):
    namespace_id = data["namespace_id"]
    namespace = namespaces_db.namespaces.find_one({"_id": namespace_id})  # 获取所有的环境
    for env in namespace["envs"]:
        delete_env(env["_id"])  # 删除所有的环境
    namespaces_db.namespaces.delete_one({"_id": namespace_id})


def get_namespace_name(namespace_id):
    print(namespace_id)
    namespace = namespaces_db.namespaces.find_one({"_id": namespace_id})
    return namespace["name"]


def serialize_env_data(namespace):
    env_ids = namespace.pop("envs")
    namespace["envs"] = []
    for env_id in env_ids:
        env = envs_db.envs.find_one({"_id": env_id})
        namespace["envs"].append(env)
    return namespace

def namespace_delete_env(namespace_id=None, env_id=None):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    namespace = namespaces_db.namespaces.find_one({"_id": namespace_id})
    envs = namespace.pop("envs")
    for env in envs:
        if env == env_id:
            envs.remove(env)
    namespaces_db.namespaces.update({"_id": namespace_id}, {"$set": {"envs": envs, "update_time": now_time}}, upsert=True)

if __name__ == '__main__':
    namespace_id = "f9f4a5fa-d348-469c-a977-02be776db4b3"
    env_id = "eae02b0e-7104-47e4-8c7b-efc4f8ea3b95"
    namespace_delete_env(namespace_id,env_id)