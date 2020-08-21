
class Section:

    day_code_dict = {
        "m": "monday",
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
        "sunday": "u"
    }

    def __init__(self, name, student_count, professor_name, room_name, day_code, start_time, end_time):

        self.name = name
        self.student_count = student_count
        self.professor_name = professor_name
        self.room_name = room_name

        self.day_code = day_code
        self.start_time = start_time
        self.end_time = end_time

        self.subject_code, self.course_code, self.section_code = self.get_codes()

        self.room = None

        self.subject = None
        self.course = None

    def get_codes(self):
        subject_code = (split_data := self.name.split(" "))[0]
        course_code, section_code = split_data[1][:3], split_data[1][3:]
        return subject_code, course_code, section_code

    def __str__(self):
        return "{} {} {}-{}: start: {}  end: {}".format(
            self.room_name,
            self.subject_code,
            self.course_code,
            self.section_code,
            self.start_time,
            self.end_time
        )
