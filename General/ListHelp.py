
def rotate_list_list(data_list_list):
    return [list(x) for x in zip(*data_list_list)]


def get_list_list_column(data_list_list, column_index):
    return [data_list[column_index] for data_list in data_list_list]


def split_list_list_by_column(data_list_list, column_index):
    rotated_list_list = rotate_list_list(data_list_list)
    return rotate_list_list(rotated_list_list[:column_index]), rotate_list_list(rotated_list_list[column_index:])


def remove_list_list_column(data_list_list, column_index):
    return rotate_list_list([data_list for i, data_list in
                             enumerate(rotate_list_list(data_list_list)) if column_index != i])


def is_none_list(data_list):
    return all(data is None for data in data_list)


def remove_list_list_none_lists(data_list_list):
    return [data_list for data_list in data_list_list if not is_none_list(data_list)]


def replace_nones(data_list, replace_value):
    return [data if data is not None else replace_value for data in data_list]
