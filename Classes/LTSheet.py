import pandas

from General import ListHelp


class LTSheet:

    """
    This is an object  Google Sheet with a specific format that has a table of information on one side and a dictionary for
    parameters
    """

    def __init__(self, title, data_list_list):

        self.title = title
        self.data_list_list = data_list_list

        self.data_frame, self.param_dict = self.get_data_frame_and_param_dict()

    def get_data_frame_and_param_dict(self):

        data_list_list, temp_list_list = [], []
        for i in range(len(self.data_list_list[0])):
            if not any(ListHelp.get_list_list_column(self.data_list_list, i)):
                data_list_list, temp_list_list = ListHelp.split_list_list_by_column(self.data_list_list, i)
                break
        temp_list_list = ListHelp.remove_list_list_none_lists(ListHelp.remove_list_list_column(temp_list_list, 0))[1:]
        param_dict = {temp_list[0]: temp_list[1] for temp_list in temp_list_list}

        col_header_count = int(param_dict["col_header_count"])

        return (
            pandas.DataFrame(data_list_list[col_header_count:],
                             columns=data_list_list[0] if col_header_count == 1 else None),
            param_dict
        )

    def sheet_to_simple_response(self):
        ret_str = ""
        for i, row in enumerate([list(x) for x in list(self.data_frame.values)]):
            if i != 0:
                ret_str += "\n"
            for c_i, cell in enumerate([c for c in row if c]):
                if c_i != 0:
                    ret_str += ":   "
                ret_str += cell
        return ret_str
