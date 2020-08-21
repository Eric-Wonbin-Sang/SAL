
class Course:

    def __init__(self, subject_code, course_code, section_list):

        self.subject_code = subject_code
        self.course_code = course_code
        self.name = self.subject_code + " " + self.course_code

        self.section_list = section_list

        self.update_section_list()

        self.subject = None

    def update_section_list(self):
        for section in self.section_list:
            section.course = self

    def __str__(self):
        return "{} {}: {}".format(
            self.subject_code,
            self.course_code,
            [section.section_code for section in self.section_list]
        )
