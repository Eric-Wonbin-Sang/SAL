import datetime
import requests
from bs4 import BeautifulSoup

from lib.StevensIT import Section, Room, Course, Subject


class Stevens:

    def __init__(self, room_schedule_url):

        self.name = "Stevens Institute of Technology"
        self.room_schedule_url = room_schedule_url

        self.room_list, self.section_list = self.get_room_list_section_list()
        self.course_list = self.get_course_list()
        self.subject_list = self.get_subject_list()

        self.time_updated = datetime.datetime.today()

        print(self.room_list_to_str())

    def get_room_list_section_list(self):
        soup = BeautifulSoup(requests.get(self.room_schedule_url).text, 'html.parser')
        main_body = soup.find_all("div", class_="panel-body")[0]

        room_name_list = [elem.text for elem in main_body.find_all("b")]
        table_list = main_body.find_all("table")

        room_list = []
        section_list = []
        for r_i, room_name in enumerate(room_name_list):
            temp_section_list = []
            for i, table_row in enumerate(table_list[r_i].find_all('tr')[1:]):
                day_code, sections = (row_contents := table_row.find_all('td'))[0].text, \
                                     [elem.get_text(separator="\n") for elem in row_contents[1:] if elem.text != ""]
                for elem in sections:
                    split_elem = elem.split("\n")
                    section_name, student_count, professor_name, times = \
                        split_elem[0][:-1].split("(") + split_elem[1][:-1].split("[")
                    start_time, end_time = [datetime.datetime.strptime(time, "%H%M") for time in times.split("-")]
                    temp_section_list.append(Section.Section(
                        section_name, student_count, professor_name, room_name, day_code, start_time, end_time))
            room_list.append(Room.Room(room_name, temp_section_list))
            section_list.extend(temp_section_list)
        return room_list, section_list

    def get_course_list(self):
        group_dict = {}
        for section in self.section_list:
            if (section.subject_code, section.course_code) not in group_dict:
                group_dict[(section.subject_code, section.course_code)] = []
            group_dict[(section.subject_code, section.course_code)] += [section]
        return [Course.Course(s_code, c_code, section_list) for (s_code, c_code), section_list in group_dict.items()]

    def get_subject_list(self):
        group_dict = {}
        for course in self.course_list:
            if course.subject_code not in group_dict:
                group_dict[course.subject_code] = []
            group_dict[course.subject_code] += [course]
        return [Subject.Subject(subject_code, course_list) for subject_code, course_list in group_dict.items()]

    def room_list_to_str(self):
        return "\n".join(str(room) for room in self.room_list)

    def section_list_to_str(self):
        return "\n".join(str(section) for section in self.section_list)

    def course_list_to_str(self):
        return "\n".join(str(course) for course in self.course_list)

    def subject_list_to_str(self):
        return "\n".join(str(subject) for subject in self.subject_list)


if __name__ == '__main__':
    Stevens("https://web.stevens.edu/roomsched/?year=2020&session=F")
