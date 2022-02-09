import json
import os
from typing import List, Optional


def get_env_array(env_name: str) -> Optional[List[str]]:
    env_str = os.getenv(env_name, '')
    if env_str and not env_str.isspace():
        return parse_json_array(env_str)
    return None


def parse_json_array(json_string: str) -> List[str]:
    try:
        array = json.loads(json_string)
        # If someone passes a string like this: '"./*.version"'
        if isinstance(array, str):
            return [array]
        return array
    except json.decoder.JSONDecodeError:
        # Not a valid JSON array, assume it is a single file
        return [json_string]

def str_to_bool(value: str) -> bool:
    if value.lower() in ('y', 'yes', 't','true', 'on', '1'):
        return True
    if value.lower() in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    raise ValueError(f'Could not parse string as bool: {value}')
