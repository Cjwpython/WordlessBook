# coding: utf-8
from flask import Flask, request
from flask import jsonify

from db import mongo_cli, get_collection_names, get_namespaces_apps

app = Flask(__name__)
namespaces_db = mongo_cli["namespaces"]


def get_namespace_apps():
    namespace_name = request.path.split("/")[-1]
    data = get_namespaces_apps(namespaces_name=namespace_name)
    return jsonify({"message": data, "code": 200}), 200


def add_namespace_url(namespce_name):
    print(namespce_name, 123123123123123)
    app.add_url_rule(f"/namespaces/{namespce_name}", view_func=get_namespace_apps, methods=['GET', ], strict_slashes=False)


collection_list = get_collection_names(db_name="namespaces")
for collection in collection_list:
    add_namespace_url(namespce_name=collection)


@app.route("/namespaces", methods=("POST", "GET"))
def add_namespaces():
    if request.method == "POST":
        # TODO 参数校验
        data = request.json
        namespace_name = data["name"]
        namespace_desc = data["desc"]
        collection_list = get_collection_names(db_name="namespaces")
        if namespace_name in collection_list:  # 命名空间存在的话，不进行操作
            return jsonify({"message": "namespaces exist", "code": 441}), 441
        row = {
            "_id": "desc",
            "desc": namespace_desc
        }
        namespaces_db[namespace_name].insert(row)  # 数据库中添加一条数据
        add_namespace_url(namespce_name=namespace_name)  # 当前应用添加一条url  当debug = True 时这里报错，调试的时候需要将debug关闭
        return jsonify({"message": "create success", "code": 201}), 201
    if request.method == "GET":
        collection_list = get_collection_names(db_name="namespaces")
        data = {}
        for collection in collection_list:
            data[collection] = {}
            data[collection]["name"] = collection
            desc = namespaces_db[collection].find_one({"_id": "desc"})
            data[collection]["desc"] = desc["desc"]
        return jsonify({"collection_list": data})


def test():
    return "123123"


@app.route("/test", methods=("GET",))
def test():
    namespce_name = "123123"
    app.add_url_rule(f"/{namespce_name}", view_func=test, methods=('GET',))
    return "12312312"
print(123123)

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=False)
