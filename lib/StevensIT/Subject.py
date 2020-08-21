
class Subject:

    def __init__(self, subject_code, course_list):

        self.subject_code = subject_code
        self.course_list = course_list

        self.update_course_list()

    def update_course_list(self):
        for course in self.course_list:
            course.subject = self
            for section in course.section_list:
                section.subject = self

    def __str__(self):
        return "{}: {}".format(
            self.subject_code,
            [course.name for course in self.course_list]
        )
