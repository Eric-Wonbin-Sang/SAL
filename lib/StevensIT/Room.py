
class Room:

    def __init__(self, name, section_list):

        self.name = name
        self.section_list = section_list

        self.update_section_list()

    def update_section_list(self):
        for section in self.section_list:
            section.room = self

    def __str__(self):
        return "{}: {}".format(
            self.name,
            [section.name for section in self.section_list]
        )
