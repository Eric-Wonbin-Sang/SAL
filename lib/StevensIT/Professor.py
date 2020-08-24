
class Professor:

    def __init__(self, name, section_list):

        self.name = name
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
            section.professor = self
