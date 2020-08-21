from lib.StevensIT.Section import Section


class Room:

    def __init__(self, html_chunk, day_code_dict):
        """
        str html_chunk: initial html part for parsing
        """
        self.html_chunk = html_chunk
        self.day_code_dict = day_code_dict

        self.name = self.get_name()
        self.day_section_list_dict = self.get_day_section_list_dict()

    def get_name(self):
        return self.html_chunk[:self.html_chunk.index(">")]

    def get_day_section_list_dict(self):
        day_section_list_dict = {}
        html_list_list = [line for line in self.html_chunk.split("\n") if "</tr><tr><td>" in line]
        if len(html_list_list) != 1:
            print("Confusing input: section list html encountered 0 or 1+ lines")
            return day_section_list_dict

        html = html_list_list[0]
        for line in html.split("<tr><td>")[1:]:
            day = line[:line.index("</td>")].lower()
            section_list = [Section(day=day, room=self, html_chunk=html_chunk, day_code_dict=self.day_code_dict)
                            for html_chunk in line.split("bgcolor=")[1:]]
            day_section_list_dict[day.lower()] = section_list
        return day_section_list_dict

    def __str__(self):
        ret_str = "Room: {}".format(self.name)
        for day in self.day_section_list_dict:
            ret_str += "\n\t{}: ".format(self.day_code_dict[day.lower()])
            for section in self.day_section_list_dict[day]:
                ret_str += "\n{}".format("\t\t" + section.__str__().replace("\n", "\n\t\t"))
        return ret_str
