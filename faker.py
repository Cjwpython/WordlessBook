# coding: utf-8
from db import mongo_cli, create_collection

mongo_cli.drop_database("namespaces")
mongo_cli.drop_database("apps")
mongo_cli.drop_database("envs")
# 构建假namsspaces
namespaces = {
    "无字天书": {
        "a": {
            "desc": "a"
        },
        "b": {
            "desc": "b"
        },
        "c": {
            "desc": "c"
        },
        "desc": {
            "desc": "无字天书"
        }

    }
}
ns_db = mongo_cli["namespaces"]

for namespace in namespaces:
    create_collection(db_name="namespaces", collection_name=namespace)
    for app in namespaces[namespace]:
        namespaces[namespace][app]["_id"] = app
        ns_db[namespace].insert_one(namespaces[namespace][app])

env_db = mongo_cli["envs"]
envs = {
    "test": {
        "无字天书": {
            "configs": {
                "test": True,
                "haha": 123,
                "papa": 123123
            }
        }
    },
    "prod": {
        "无字天书": {
            "configs": {
                "test": True,
                "haha": 123,
                "papa": 123123
            }
        }
    },
    "local": {
        "无字天书": {
            "configs": {
                "test": True,
                "haha": 123,
                "papa": 123123
            }
        }
    }
}
for env in envs:
    create_collection(db_name="envs", collection_name=env)
    for app in envs[env]:
        envs[env][app]["_id"] = app
        env_db[env].insert_one(envs[env][app])

app_db = mongo_cli["apps"]
apps = {
    "无字天书": {
        "current_env": "test",
        "envs": ["test", "prod", "local"]
    }
}

for app in apps:
    create_collection(db_name="apps", collection_name=app)
    for app in apps:
        apps[app]["_id"] = app
        app_db[app].insert_one(apps[app])
