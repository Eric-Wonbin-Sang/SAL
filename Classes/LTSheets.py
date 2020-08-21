from lib import Google

from Classes import LTSheet


class LTSheets(Google.SpreadSheet):

    def __init__(self, google_sheets_credentials_json):

        super().__init__("LT Sheets", google_sheets_credentials_json)

        self.helps_sheet_title = "help_sheet"

        self.help_dict = self.get_help_dict()
        self.lt_sheet_list = self.get_lt_sheet_list()

    def get_help_dict(self):

        def data_list_list_to_str(some_list_list):
            ret_str = ""
            for i, some_list in enumerate(some_list_list):
                if i != 0:
                    ret_str += "\n"
                ret_str += "     ".join([data if data is not None else "" for data in some_list])
            return ret_str.strip()

        helps_l_l = self.sheet_to_list_list(self.helps_sheet_title)
        command_index_list = [i for i, data_list in enumerate(helps_l_l) if data_list[0] is not None] + [len(helps_l_l)]
        command_help_dict = {}
        for i, command_index in enumerate(command_index_list[:-1]):
            data_list_list = helps_l_l[command_index:command_index_list[i + 1]]
            command_help_dict[data_list_list[0][0]] = \
                data_list_list_to_str([data_list[1:] for data_list in data_list_list])
        return command_help_dict

    def get_lt_sheet_list(self):
        sheets_to_ignore = [self.helps_sheet_title]
        return [LTSheet.LTSheet(sheet.title, self.sheet_to_list_list(sheet.title)) for sheet in self.sheet_list
                if sheet.title not in sheets_to_ignore]

    def get_lt_sheet(self, lt_sheet_title):
        for lt_sheet in self.lt_sheet_list:
            if lt_sheet.title == lt_sheet_title:
                return lt_sheet
        return None
