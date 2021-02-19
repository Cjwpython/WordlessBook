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
