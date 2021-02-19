# coding: utf-8

create_env_validate = {
    "type": "object", "properties": {
        "name": {"type": "string"},
        "nick_name": {"type": "string"},
        "namespace_id": {"type": "string"}
    },
    "required": ["name", "nick_name", "namespace_id"],
    "additionalProperties": False  # 不接受规定以外的数个传入，True 除了必传的参数外，接受其他参数的传入
}

update_env_validate = {
    "type": "object", "properties": {
        "env_id": {"type": "string"},
        "nick_name": {"type": "string"}
    },
    "required": ["env_id", "nick_name"],
    "additionalProperties": False
}

delete_env_validate = {
    "type": "object", "properties": {
        "env_id": {"type": "string"}
    },
    "required": ["env_id"],
    "additionalProperties": False
}

env_change_namespace_validate = {
    "type": "object", "properties": {
        "env_id": {"type": "string"},
        "namespace_id": {"type": "string"},
        "current_namespace_id": {"type": "string"},
    },
    "required": ["env_id", "namespace_id", "current_namespace_id"],
    "additionalProperties": False
}
