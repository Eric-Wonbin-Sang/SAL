import os
import json


def str_to_length(base_str, length, do_dots=True):
    ret_str = base_str.ljust(length)[:length]
    if do_dots and base_str + 3 >= length:
        return ret_str[:-3] + "..."
    return ret_str


def get_curr_parent_dir():
    return os.path.dirname(os.getcwd()).replace("\\", "/")


def parse_json(json_path):
    if not os.path.exists(json_path):
        raise FileExistsError
    with open(json_path) as f:
        return json.load(f)


def get_pretty_time(some_datetime):
    return some_datetime.strftime("%I:%M%p")


def txt_to_dict(txt_path):
    ret_dict = {}
    for line in open(txt_path):
        key, value = [obj.strip() for obj in line.split(":")]
        ret_dict[key] = value
    return ret_dict


def data_frame_to_list_list(data_frame):
    return [list(x) for x in list(data_frame.values)]
