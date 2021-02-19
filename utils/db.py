# coding: utf-8
from pymongo import MongoClient

mongo_server = "10.0.83.98"
mongo_uri = 'mongodb://cyberivy:cyberivy@%s/' % mongo_server


class MongoClientSingleton(object):
    '''通过重载实例化函数__new__缓存mongodb连接'''
    conn = None

    def __new__(cls, *args, **kwds):
        if cls.conn is None:
            cls.conn = MongoClient(mongo_uri)
        return cls.conn


mongo_cli = MongoClientSingleton()

namespaces_db = mongo_cli["namespaces"]
envs_db = mongo_cli["envs"]
apps_db = mongo_cli["applications"]


def check_db_exist(db_name=None):
    dblist = mongo_cli.list_database_names()
    if db_name in dblist:
        return True
    return False


def get_collection_names(db_name=None):
    """

    :param db_name: db name
    :return: coll in db all names
    """
    if not check_db_exist(db_name=db_name):
        return []
    db = mongo_cli[db_name]
    collection_list = db.list_collection_names(session=None)
    if not collection_list:
        return []
    if "desc" in collection_list:
        collection_list.remove("desc")
    return collection_list


def check_collection_in_db(db_name=None, collection_name=None):
    """

    :param db_name: db name
    :param collection_name: db.coll name
    :return: coll in db all names
    """
    if not check_db_exist(db_name=db_name):
        return False
    db = mongo_cli[db_name]
    collection_list = db.list_collection_names(session=None)
    if collection_name not in collection_list:
        return False
    return True


def create_collection(db_name=None, collection_name=None):
    if not check_db_exist(db_name=db_name):
        return False
    if not check_collection_in_db(db_name=db_name, collection_name=collection_name):
        db = mongo_cli[db_name]
        db.create_collection(collection_name)
        return True
    return False


def get_namespaces_apps(namespaces_name=None):
    all_apps = namespaces_db[namespaces_name].find()
    data = {}
    for app in all_apps:
        if app["_id"] == "desc":
            continue
        name = app.pop("_id")
        data[name] = {}
        data[name]["name"] = name
        data[name]["desc"] = app["desc"]
    return data


if __name__ == '__main__':
    # print(check_db_exist(db_name="namespaces"))
    # print(get_collection_names(db_name="namespaces"))
    # print(check_collection_in_db(db_name="namespaces", collection_name="123123"))
    get_namespaces_apps(namespaces_name="无字天书")
