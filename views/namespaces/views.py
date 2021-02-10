# coding: utf-8
import datetime
import uuid
from pprint import pprint

from flask import jsonify, views, request

from utils.db import namespaces_db
import logging

logging.getLogger("test.views")


def get_list_namespaces():
    data = {}
    data["namespaces"] = []
    max_count = namespaces_db.namespaces.find().count()

    params = request.args.to_dict(flat=True)
    current_page = params.get("current_page", 1)
    current_max_row = params.get("current_max_row", 15)
    sort_type = params.get("sort_type", "create_time")
    skip = (current_page - 1) * current_max_row
    if sort_type not in ["create_time", "update_time"]:
        sort_type = "create_time"
    namespaces = namespaces_db.namespaces.find({}, {"name": 1, "nick_name": 1}).sort(sort_type, -1).skip(skip).limit(current_max_row)  # 只返回名称和昵称
    for namespace in namespaces:
        data["namespaces"].append(namespace)
        print(namespace)
    data["max_count"] = max_count
    data["current_page"] = current_page
    data["current_max_row"] = current_max_row
    data["sort_type"] = sort_type
    return jsonify({"data": data}), 200


def get_single_namespace(namespace_id):
    data = []
    namespace = namespaces_db.namespaces.find_one({"_id": namespace_id})
    if namespace:
        data.append(namespace)
    return jsonify({"data": data}), 200


class Namespace(views.MethodView):

    def post(self):
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        name = request.json.get("name")
        _namespace = namespaces_db.namespaces.find_one({"name": name})
        if _namespace:
            return jsonify({"code": 400, "message": f"{name}命名空间已存在"}), 400
        namespace = {
            "_id": str(uuid.uuid4()),
            "name": name,
            "nick_name": request.json.get("nick_name"),
            "create_time": now_time,
            "update_time": now_time
        }

        namespaces_db.namespaces.insert_one(namespace)
        return jsonify({"code": 201, "message": "创建成功"}), 201

    def put(self):
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        namespace_id = request.json.get("namespace_id")
        nick_name = request.json.get("nick_name")
        namespace = namespaces_db.namespaces.find_one({"_id": namespace_id})
        if not namespace:
            return jsonify({"code": 400, "message": "命名空间不存在"}), 400
        namespaces_db.namespaces.update({"_id": namespace_id}, {"$set": {"nick_name": nick_name, "update_time": now_time}}, upsert=True)
        return jsonify({"code": 200, "message": "更新成功"}), 200

    def delete(self):
        namespace_id = request.json.get("namespace_id")
        namespace = namespaces_db.namespaces.find_one({"_id": namespace_id})
        if not namespace:
            return jsonify({"code": 400, "message": "命名空间不存在"}), 400
        namespaces_db.namespaces.delete_one({"_id": namespace_id})
        return jsonify({"code": 200, "message": "删除成功"}), 200
