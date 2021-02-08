# coding: utf-8
import uuid
from pprint import pprint

from flask import jsonify, views, request

from utils.db import namespaces_db
import logging

logging.getLogger("test.views")


def get_all_namespaces():
    data = []
    namespaces = namespaces_db.namespaces.find({}, {"name": 1, "nick_name": 1})  # 只返回名称和昵称
    for namespace in namespaces:
        data.append(namespace)
    return jsonify({"data": data}), 200


def get_single_namespace(namespace_id):
    data = []
    namespace = namespaces_db.namespaces.find_one({"_id": namespace_id})
    if namespace:
        data.append(namespace)
    return jsonify({"data": data}), 200


class Namespace(views.MethodView):

    def post(self):
        namespace = {
            "_id": str(uuid.uuid4()),
            "name": request.json.get("name"),
            "nick_name": request.json.get("nick_name")
        }
        namespaces_db.namespaces.insert_one(namespace)
        return jsonify({"code": 201, "message": "创建成功"}), 201

    def put(self):
        namespace_id = request.json.get("namespace_id")
        name = request.json.get("name")
        nick_name = request.json.get("nick_name")
        namespace = namespaces_db.namespaces.find_one({"_id": namespace_id})
        if not namespace:
            return jsonify({"code": 400, "message": "命名空间不存在"}), 400
        namespaces_db.namespaces.update({"_id": namespace_id}, {"name": name, "nick_name": nick_name})
        return jsonify({"code": 200, "message": "更新成功"}), 200

    def delete(self):
        namespace_id = request.json.get("namespace_id")
        namespace = namespaces_db.namespaces.find_one({"_id": namespace_id})
        if not namespace:
            return jsonify({"code": 400, "message": "命名空间不存在"}), 400
        namespaces_db.namespaces.delete_one({"_id": namespace_id})
        return jsonify({"code": 200, "message": "删除成功"}), 200
