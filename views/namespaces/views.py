# coding: utf-8
import datetime
import uuid
from pprint import pprint

from flask import jsonify, views, request
from middleware.validate import check_date
from utils.db import namespaces_db
import logging

from views.namespaces.validate import create_namespace_validate, update_namespace_validate, delete_namespace_validate

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
    return jsonify({"data": data, "status_code": 200}), 200


def get_single_namespace(namespace_id):
    data = []
    namespace = namespaces_db.namespaces.find_one({"_id": namespace_id})
    if namespace:
        data.append(namespace)
    return jsonify({"data": data, "status_code": 200}), 200


class Namespace(views.MethodView):
    @check_date(schema=create_namespace_validate)
    def post(self):
        data = request.json
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        name = data["name"]
        _namespace = namespaces_db.namespaces.find_one({"name": name})
        if _namespace:
            return jsonify({"status_code": 400, "message": f"{name}命名空间已存在"}), 400
        namespace = {
            "_id": str(uuid.uuid4()),
            "name": name,
            "nick_name": data["nick_name"],
            "create_time": now_time,
            "update_time": now_time
        }

        namespaces_db.namespaces.insert_one(namespace)
        return jsonify({"status_code": 201, "message": "创建成功"}), 201

    @check_date(schema=update_namespace_validate)
    def put(self):
        data = request.json
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        namespace_id = data["namespace_id"]
        nick_name = data["nick_name"]
        namespace = namespaces_db.namespaces.find_one({"_id": namespace_id})
        if not namespace:
            return jsonify({"status_code": 400, "message": "命名空间不存在"}), 400
        namespaces_db.namespaces.update({"_id": namespace_id}, {"$set": {"nick_name": nick_name, "update_time": now_time}}, upsert=True)
        return jsonify({"status_code": 200, "message": "更新成功"}), 200

    @check_date(schema=delete_namespace_validate)
    def delete(self):
        data = request.json
        namespace_id = data["namespace_id"]
        namespace = namespaces_db.namespaces.find_one({"_id": namespace_id})
        if not namespace:
            return jsonify({"status_code": 400, "message": "命名空间不存在"}), 400
        namespaces_db.namespaces.delete_one({"_id": namespace_id})
        return jsonify({"status_code": 200, "message": "删除成功"}), 200
