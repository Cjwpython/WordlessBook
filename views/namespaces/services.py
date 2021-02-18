# coding: utf-8
import uuid
import datetime

from utils.db import namespaces_db
from utils.errors import NamespaceExist, NamespaceNotExist


def create_namespace(data):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    namespace = {
        "_id": str(uuid.uuid4()),
        "name": data["name"],
        "nick_name": data["nick_name"],
        "create_time": now_time,
        "update_time": now_time,
        "envs": {}
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
    namespaces_db.namespaces.delete_one({"_id": namespace_id})
