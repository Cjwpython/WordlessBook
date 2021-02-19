# coding: utf-8
import datetime
import uuid

from utils.db import envs_db, apps_db
from utils.errors import ApplicationExist, ApplicationNotExist, ConfigTypeError


def create_application(data):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 创建一个环境
    app = {
        "_id": str(uuid.uuid4()),
        "name": data["name"],
        "nick_name": data["nick_name"],
        "env_id": data["env_id"],
        "create_time": now_time,
        "update_time": now_time,
        "configs": {}
    }
    apps_db.apps.insert_one(app)
    # env中插入数据
    env_add_application(env_id=data["env_id"], application_id=app["_id"])
    return app["_id"]


def env_add_application(env_id=None, application_id=None):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    envs_db.envs.update(
        {"_id": env_id},
        {
            "$addToSet": {"apps": application_id},
            "$set": {"update_time": now_time}}
    )


def check_application_exist_by_id(application_id, raise_exist=True):
    application = apps_db.apps.find_one({"_id": application_id})
    if application and raise_exist:
        raise ApplicationExist
    if not application and not raise_exist:
        raise ApplicationNotExist
    return application


def check_env_exist_application(env_id, application_name, raise_exist=True):
    apps = apps_db.apps.find({"name": application_name})
    for app in apps:
        if not app:
            return
        if env_id == app["env_id"] and raise_exist:
            raise ApplicationExist


def check_env_exist_application_by_id(env_id, application_id):
    env = envs_db.envs.find_one({"_id": env_id})
    if application_id in env["apps"]:
        raise ApplicationExist


def delete_application(appliction_id):
    apps_db.apps.delete_one({"_id": appliction_id})


def env_delete_application(env_id=None, application_id=None):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    env = envs_db.envs.find_one({"_id": env_id})
    apps = env.pop("apps")
    try:
        apps.remove(application_id)
    except Exception as e:
        pass
    envs_db.envs.update({"_id": env_id}, {"$set": {"apps": apps, "update_time": now_time}}, upsert=True)


def update_application_env_id(application_id, env_id):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    apps_db.apps.update(
        {"_id": application_id},
        {
            "$set": {"update_time": now_time, "env_id": env_id}}
    )


def update_application_configs(application_id=None, configs=None):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    """
    configs = [
    {
        "key": "123",
        "value": 123,
        "type": "int"
    },
    {
        "key": "234",
        "value": 0.99,
        "type": "float"
    },
    {
        "key": "mongourl",
        "value": "10.0.81.9",
        "type": "str"
    },
    {
        "key": "list",
        "value": [1, 2, 3],
        "type": "list"
    },
    {
        "key": "dict",
        "value": {1: 2, 3: 4},
        "type": "dict"
    }
]
    """
    data = {}
    for config in configs:
        key = config["key"]
        value = config["value"]
        type = config["type"]
        if type == "int":
            if not isinstance(value, int):
                raise ConfigTypeError(f"{key}的格式非{type}")
        elif type == "list":
            if not isinstance(value, list):
                raise ConfigTypeError(f"{key}的格式非{type}")
        elif type == "float":
            if not isinstance(value, float):
                raise ConfigTypeError(f"{key}的格式非{type}")
        elif type == "dict":
            if not isinstance(value, dict):
                raise ConfigTypeError(f"{key}的格式非{type}")
        elif type == "str":
            if not isinstance(value, str):
                raise ConfigTypeError(f"{key}的格式非{type}")
        else:
            raise ConfigTypeError(f"{key}的格式{type}，不在默认格式中")
        data[key] = value
    apps_db.apps.update(
        {"_id": application_id},
        {
            "$set": {"update_time": now_time, "configs": data}}
    )
