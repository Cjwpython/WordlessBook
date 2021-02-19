# coding: utf-8
import datetime
import uuid

from utils.db import envs_db, apps_db
from utils.errors import ApplicationExist, ApplicationNotExist


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


def env_delete_application(env_id=None, application_id=None):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    env = envs_db.envs.find_one({"_id": env_id})
    apps = env.pop("apps")
    for app in apps:
        if app == application_id:
            apps.remove(app)
    envs_db.envs.update({"_id": env_id}, {"$set": {"envs": apps, "update_time": now_time}}, upsert=True)
