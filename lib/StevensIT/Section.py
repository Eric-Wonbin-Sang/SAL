import datetime

from General import Functions


class Section:

    def __init__(self, day, room, html_chunk, day_code_dict):
        """
        str day
        str html_chunk: initial html part for parsing
        """

        self.day = day
        self.room = room
        self.html_chunk = html_chunk
        self.day_code_dict = day_code_dict

        self.course_name, self.professor, self.start_time, self.end_time = self.get_data()

    def get_data(self):
        line = self.html_chunk.split("colspan=")[1]
        raw_course_name = line.split("<br>")[0].split(">")[1].split("(")[0]
        raw_professor, raw_times = line.split("<br>")[1].split("[")

        raw_times = raw_times[:-1].split("-")
        raw_times[1] = raw_times[1].split("]")[0]

        course_name = raw_course_name
        professor = raw_professor
        start_time = datetime.time(int(raw_times[0][:-2]), int(raw_times[0][-2:]))
        end_time = datetime.time(int(raw_times[1][:-2]), int(raw_times[1][-2:]))

        return course_name, professor, start_time, end_time

    def __str__(self, do_one_line=False):
        if not do_one_line:
            return "Course Name: {}\nProfessor: {}\nStart Time: {}\nEnd Time: {}\n".format(
                self.course_name,
                self.professor,
                self.start_time,
                self.end_time)
        return "{}: {} - {} | {} ({})".format(
            self.day_code_dict[self.day.lower().lower()][:3].title(),
            Functions.get_pretty_time(self.start_time),
            Functions.get_pretty_time(self.end_time),
            self.course_name,
            self.professor)
