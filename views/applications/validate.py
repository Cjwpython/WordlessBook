# coding: utf-8

create_app_validate = {
    "type": "object", "properties": {
        "name": {"type": "string"},
        "nick_name": {"type": "string"},
        "namespace_id": {"type": "string"},
        "env_id": {"type": "string"}
    },
    "required": ["name", "nick_name", "namespace_id", "env_id"],
    "additionalProperties": True
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
