import flask

def check_fields(d: dict, fields: list[str]) -> bool:
    """Takes a dictionary and returns true if all keys
    listed in fields are contained within"""

    keys = d.keys()
    return all(field in keys for field in fields)