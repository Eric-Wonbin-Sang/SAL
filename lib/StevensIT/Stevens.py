import datetime
import requests

from lib.StevensIT.Room import Room


class Stevens:

    day_code_dict = {"m": "monday",
                     "t": "tuesday",
                     "w": "wednesday",
                     "r": "thursday",
                     "f": "friday",
                     "s": "saturday",
                     "u": "sunday",
                     "monday": "m",
                     "tuesday": "t",
                     "wednesday": "w",
                     "thursday": "r",
                     "friday": "f",
                     "saturday": "s",
                     "sunday": "u"}

    def __init__(self, room_schedule_url):

        self.name = "StevensIT Institute of Technology"

        self.room_schedule_url = room_schedule_url
        self.room_list = self.get_room_list()
        self.prof_section_list_dict = self.get_prof_section_list_dict()

        self.time_updated = datetime.datetime.today()

    def get_room_list(self):
        r = requests.get(self.room_schedule_url)
        return [Room(html_chunk, day_code_dict=self.day_code_dict) for html_chunk in r.text.split('<b id=')[1:]]

    def get_prof_section_list_dict(self):
        prof_section_list_dict = {}
        for room in self.room_list:
            for day_key in room.day_section_list_dict:
                for section in room.day_section_list_dict[day_key]:
                    if section.professor in prof_section_list_dict:
                        prof_section_list_dict[section.professor] += [section]
                    else:
                        prof_section_list_dict[section.professor] = [section]
        return prof_section_list_dict

    def find_schedule(self):
        pass
