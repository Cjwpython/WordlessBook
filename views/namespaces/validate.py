# coding: utf-8

create_namespaces_validate = {
    "type": "object", "properties": {
        "name": {"type": "string"},
        "nick_name": {"type": "string"}
    },
    "required": ["name", "nick_name"],
    "additionalProperties": False  # 不接受规定以外的数个传入，True 除了必传的参数外，接受其他参数的传入
}

update_namespaces_validate = {
    "type": "object", "properties": {
        "namespace_id": {"type": "string"},
        "nick_name": {"type": "string"}
    },
    "required": ["namespace_id", "nick_name"],
    "additionalProperties": False
}

delete_namespaces_validate = {
    "type": "object", "properties": {
        "namespace_id": {"type": "string"}
    },
    "required": ["namespace_id"],
    "additionalProperties": False
}
