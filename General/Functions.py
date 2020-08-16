import os
import json


def get_curr_parent_dir():
    return os.path.dirname(os.getcwd()).replace("\\", "/")


def parse_json(json_path):
    if not os.path.exists(json_path):
        raise FileExistsError
    with open(json_path) as f:
        return json.load(f)


def get_pretty_time(some_datetime):
    some_datetime.strftime("%I:%M%p")


def txt_to_dict(txt_path):
    ret_dict = {}
    for line in open(txt_path):
        key, value = [obj.strip() for obj in line.split(":")]
        ret_dict[key] = value
    return ret_dict
