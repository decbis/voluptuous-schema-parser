def get_key_dict(field_name, is_required):
    return {"name": field_name, 
            "is_required": is_required}

def get_value_dict(requirements):
    return {"requirements": requirements}

def get_field_dict(key_dict, value_dict):
    return {"key": key_dict, 
            "value": value_dict}
