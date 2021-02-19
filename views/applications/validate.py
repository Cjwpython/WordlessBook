# coding: utf-8

create_app_validate = {
    "type": "object", "properties": {
        "name": {"type": "string"},
        "nick_name": {"type": "string"},
        "env_id": {"type": "string"}
    },
    "required": ["name", "nick_name", "env_id"],
    "additionalProperties": True
}

update_application_validate = {
    "type": "object", "properties": {
        "application_id": {"type": "string"},
        "nick_name": {"type": "string"}
    },
    "required": ["application_id", "nick_name"],
    "additionalProperties": False
}

delete_application_validate = {
    "type": "object", "properties": {
        "application_id": {"type": "string"}
    },
    "required": ["application_id"],
    "additionalProperties": False
}
application_change_env_validate = {
    "type": "object", "properties": {
        "env_id": {"type": "string"},
        "application_id": {"type": "string"},
        "current_env_id": {"type": "string"},
    },
    "required": ["env_id", "application_id", "current_env_id"],
    "additionalProperties": False
}

create_config_validate = {
    "type": "object", "properties": {
        "configs": {"type": "array"}
    },
    "required": ["configs"],
    "additionalProperties": False
}
