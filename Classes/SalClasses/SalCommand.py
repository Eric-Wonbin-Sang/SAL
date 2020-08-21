from Classes import Command


class SalCommand(Command.Command):

    def __init__(self, lt_sheets, command_name, function, requires_args):

        self.lt_sheets = lt_sheets

        super().__init__(command_name, function, requires_args)

        self.update_function()
        self.update_help()

    def update_function(self):
        lt_sheet = self.lt_sheets.get_lt_sheet(self.name)
        if self.function is None and lt_sheet is not None:
            self.function = lt_sheet.sheet_to_simple_response

    def update_help(self):
        if new_help := self.lt_sheets.help_dict.get(self.name):
            self.help = new_help
