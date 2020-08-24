
class Room:

    def __init__(self, name, section_list):

        self.name = name.lower()
        self.section_list = section_list

        self.day_section_list_dict = self.get_day_section_list_dict()

        self.update_section_list()

    def get_day_section_list_dict(self):
        day_section_list_dict = {}
        for section in self.section_list:
            if section.day_code not in day_section_list_dict:
                day_section_list_dict[section.day_code] = []
            day_section_list_dict[section.day_code] += [section]
        return day_section_list_dict

    def update_section_list(self):
        for section in self.section_list:
            section.room = self

    def day_section_list_dict_to_str(self):
        return " | ".join(["{}: {}".format(day_code, ", ".join(section.name for section in section_list))
                          for day_code, section_list in self.day_section_list_dict.items()])

    def __str__(self):
        return "{}: {}".format(
            self.name,
            [section.name for section in self.section_list]
        )
