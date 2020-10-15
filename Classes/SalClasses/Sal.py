import datetime
import pyjokes
import random

from lib import GroupMe, Weather
from lib.StevensIT.Stevens import Stevens

from Classes import EnvProfile, LTSpreadsheet, Command, Bictionary
from General import Functions


class Sal(GroupMe.Bot):

    day_code_bict = Bictionary.Bictionary(
        {
            "m": "monday",
            "t": "tuesday",
            "w": "wednesday",
            "r": "thursday",
            "f": "friday",
            "s": "saturday",
            "u": "sunday"
        }
    )

    def __init__(self, env_key, do_startup_message):

        self.env_profile = EnvProfile.EnvProfile(env_key=env_key)
        print("SAL: getting LTSpreadsheet information... ", end="")
        self.lt_spreadsheet = LTSpreadsheet.LTSpreadsheet(self.env_profile.common_dict["google_sheets_creds"])
        print("done!")
        print("SAL: getting Stevens course information... ", end="")
        self.stevens = Stevens(room_schedule_url=self.get_room_schedule_url())
        print("done!")

        super().__init__(
            name=self.env_profile.profile_dict["name"],
            call_code=self.env_profile.profile_dict["call_code"],
            bot_id=self.env_profile.profile_dict["credentials_json"]["bot_id"],
            groupchat_id=self.env_profile.profile_dict["credentials_json"]["groupchat_id"],
            groupme_access_token=open(self.env_profile.common_dict["groupme_access_token"]).read(),
            startup_message=self.lt_spreadsheet.help_dict["help"],
            do_startup_message=do_startup_message
        )

        self.sal_command_list = self.get_sal_command_list(
            [
                ("room", self.room_response, True),
                ("prof", self.prof_response, True),
                ("box", None, False),
                ("contact", None, False),
                ("urls", None, False),
                ("work", self.work_response, True),
                ("lamp", None, False),
                ("update", self.update_response, False),
                ("weather", self.weather_response, False),
                ("joke", self.joke_response, False),
            ]
        )

        print("SAL has been initiated.")
        print("-----------------------------")

    def get_sal_command_list(self, tuple_list):
        sal_command_list = []
        for name, function, requires_args in tuple_list:
            lt_sheet = self.lt_spreadsheet.get_lt_sheet(name)
            function = lt_sheet.sheet_to_simple_response if function is None and lt_sheet else function
            command_help = self.lt_spreadsheet.help_dict.get(name, "Help does not exist!")
            sal_command_list.append(
                Command.Command(name=name, function=function, requires_args=requires_args, command_help=command_help)
            )
        return sal_command_list

    def get_room_schedule_url(self):
        data_frame = self.lt_spreadsheet.get_lt_sheet("urls").data_frame
        return data_frame.loc[data_frame["Website"] == "Room Schedule"].iloc[0]["URL"]

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
        if message is not None and message.name != self.name and self.is_bot_called(message):
            command_list_list = self.get_command_list_list(message.text)
            if command_list_list:
                for (command, *arg_list) in command_list_list:
                    if (sal_command := self.get_sal_command(command)) is not None:
                        self.write_text(sal_command.run(arg_list))
                    else:
                        self.write_text("The {} command does not exist!".format(command))
            else:
                if message.text == "sal":
                    self.write_text(self.startup_message)

    def room_response(self, arg_list):
        """ This function will always run with at least one arg because the of the command class's required_args. """
        room_name, *day_code_list = arg_list
        room_list = [room for room in self.stevens.room_list if room_name in room.name.lower()]

        if not room_list:
            return "No rooms found with {} prefix".format(room_name)
        elif len(room_list) > 1:
            return "Multiple rooms found: " + ", ".join([room.name.upper() for room in room_list])

        if not day_code_list:
            day_code_list.append(self.day_code_bict.find(datetime.datetime.now().strftime("%A").lower()))
        day_code_list = [dc.lower() for dc in day_code_list if self.day_code_bict.exists(dc)]
        day_code_list = [dc if len(dc) < 2 else self.day_code_bict.find(dc) for dc in day_code_list]

        room = room_list[0]
        ret_str = "Room {}: searching for {}".format(
            room.name.upper(),
            ", ".join([self.day_code_bict.find(dc) for dc in day_code_list if self.day_code_bict.exists(dc)])
        )
        for day_code in day_code_list:
            ret_str += "\n{}".format(self.day_code_bict.find(day_code).title())
            if section_list := room.day_section_list_dict.get(day_code):
                for section in section_list:
                    ret_str += "\n\t{} - {}: {} ({})".format(
                        Functions.get_pretty_time(section.start_time),
                        Functions.get_pretty_time(section.end_time),
                        section.name,
                        section.professor_name
                    )
            else:
                ret_str += "\n\tNo sections on this day"
        return ret_str

    def prof_response(self, arg_list):
        prof_name = " ".join(arg_list)
        prof_list = [prof for prof in self.stevens.professor_list if prof_name in prof.name.lower()]
        professor = None
        for prof in prof_list:
            if prof.name.lower() == prof_name:
                professor = prof

        if not prof_list:
            return "No professors with name {}".format(prof_name)
        elif len(prof_list) > 1 and professor is None:
            return "Multiple professors found: " + ", ".join([prof.name.title() for prof in prof_list])

        ret_str = "Professor {}:".format(professor.name)
        ret_str += "\n-------------"
        for day_code, section_list in professor.day_section_list_dict.items():
            ret_str += "\n" + self.day_code_bict.find(day_code).title()
            for section in section_list:
                ret_str += "\n\t" + "{} - {}: Room {} - {}".format(
                    Functions.get_pretty_time(section.start_time),
                    Functions.get_pretty_time(section.end_time),
                    section.room_name,
                    section.name
                )
        return ret_str

    def work_response(self):
        return "incomplete"

    def update_response(self):
        return "incomplete"

    def weather_response(self, city="hoboken"):
        weather = Weather.Weather(self.env_profile.common_dict["yahoo_weather_api_json"])
        return weather.get_response(city)

    def joke_response(self):
        if random.random() < .5:
            return "Evan Thomas Romeo"
        return pyjokes.get_joke()
