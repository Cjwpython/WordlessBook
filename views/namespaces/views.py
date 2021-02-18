# coding: utf-8
from flask import jsonify, views, request
from middleware.validate import check_date
from utils.db import namespaces_db
import logging

from views.namespaces.services import create_namespace, update_namespace, check_namespaces_exist_by_name, check_namespaces_exist_by_id, delete_namespace
from views.namespaces.validate import create_namespace_validate, update_namespace_validate, delete_namespace_validate

logging.getLogger("test.views")


def get_list_namespaces():
    data = {}
    data["namespaces"] = []
    max_count = namespaces_db.namespaces.find().count()

    params = request.args.to_dict(flat=True)
    current_page = params.get("current_page", 1)
    current_max_row = params.get("current_max_row", 15)
    sort_type = params.get("sort_type", "update_time")
    skip = (int(current_page) - 1) * int(current_max_row)
    if sort_type not in ["create_time", "update_time"]:
        sort_type = "update_time"
    namespaces = namespaces_db.namespaces.find(
        {},
        {"name": 1, "nick_name": 1}).sort(sort_type, -1).skip(int(skip)).limit(int(current_max_row))  # 只返回名称和昵称
    for namespace in namespaces:
        data["namespaces"].append(namespace)
    data["max_count"] = max_count
    data["current_page"] = current_page
    data["current_max_row"] = current_max_row
    data["sort_type"] = sort_type
    return jsonify({"data": data, "status_code": 200}), 200


def get_single_namespace(namespace_id):
    check_namespaces_exist_by_id(id=namespace_id, raise_exist=False)
    namespace = namespaces_db.namespaces.find_one({"_id": namespace_id})
    return jsonify({"data": namespace, "status_code": 200}), 200


class Namespace(views.MethodView):
    @check_date(schema=create_namespace_validate)
    def post(self):
        data = request.json
        check_namespaces_exist_by_name(name=data["name"], raise_exist=True)
        namespace_id = create_namespace(data)
        return jsonify({"status_code": 201, "message": f"{namespace_id} 创建成功"}), 201

    @check_date(schema=update_namespace_validate)
    def put(self):
        data = request.json
        check_namespaces_exist_by_id(id=data["namespace_id"], raise_exist=False)
        update_namespace(data)
        return jsonify({"status_code": 200, "message": "更新成功"}), 200

    @check_date(schema=delete_namespace_validate)
    def delete(self):
        data = request.json
        check_namespaces_exist_by_id(id=data["namespace_id"], raise_exist=False)
        delete_namespace(data)
        return jsonify({"status_code": 200, "message": "删除成功"}), 200
