from lib import GroupMe, Stevens

from Classes import EnvProfile, LTSheets, Command


class Sal(GroupMe.Bot):

    def __init__(self, env_key):

        self.env_profile = EnvProfile.EnvProfile(env_key=env_key)
        self.lt_sheets = LTSheets.LTSheets(self.env_profile.common_dict["google_sheets_creds"])
        # self.stevens = Stevens.Stevens(room_schedule_url=self.env_profile.common_dict["google_sheets_creds"])

        super().__init__(name=self.env_profile.profile_dict["name"],
                         call_code=self.env_profile.profile_dict["call_code"],
                         bot_id=self.env_profile.profile_dict["credentials_json"]["bot_id"],
                         groupchat_id=self.env_profile.profile_dict["credentials_json"]["groupchat_id"],
                         groupme_access_token=open(self.env_profile.common_dict["groupme_access_token"]).read(),
                         startup_message=self.lt_sheets.help_dict["help"])

        self.sal_command_list = [
            SalCommand(self.lt_sheets, "room", self.room_response, requires_args=True),
            SalCommand(self.lt_sheets, "prof", None, requires_args=True),
            SalCommand(self.lt_sheets, "box", None, requires_args=False),
            SalCommand(self.lt_sheets, "contact", None, requires_args=False),
            SalCommand(self.lt_sheets, "urls", None, requires_args=False),
            SalCommand(self.lt_sheets, "work", None, requires_args=True),
            SalCommand(self.lt_sheets, "lamp", None, requires_args=False),
            SalCommand(self.lt_sheets, "update", None, requires_args=False)
        ]

    def get_sal_command(self, command_name):
        for sal_command in self.sal_command_list:
            if command_name == sal_command.name:
                return sal_command
        return None

    def get_command_list_list(self, text):
        word_list = text.lower().split(" ")
        command_index_list = [i for i, word in enumerate(word_list) if word in
                              [sal_command.name for sal_command in self.sal_command_list]] + [len(word_list)]
        command_list_list = []
        for i, index in enumerate(command_index_list[:-1]):
            command_list_list.append(word_list[index:command_index_list[i + 1]])
        return command_list_list

    def handle_response(self, message):
        if message.name != self.name and self.is_bot_called(message):
            command_list_list = self.get_command_list_list(message.text)
            if command_list_list:
                for (command, *arg_list) in command_list_list:
                    if (sal_command := self.get_sal_command(command)) is not None:
                        self.write_text(sal_command.run(arg_list))
                    else:
                        self.write_text("The {} command does not exist!".format(command))
            else:
                self.write_text("IDK WHAT THAT IS")

    def room_response(self, arg_list):
        return "yes"


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
        print(self.function)

    def update_help(self):
        if new_help := self.lt_sheets.help_dict.get(self.name):
            self.help = new_help
