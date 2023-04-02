import copy

from course import _Course
from focus import *  # also imports course
# from CourseGraph import Graph

def schedule(in_path: set[_Course], completed_courses: set[_Course], current_semester: str, max_courses_in_semster: int = 5) -> dict[str, set[_Course]]:
    """Returns one of the faster way to complete a focus
    Preconditions:
    current_semester is in ('Fall' + 'Winter') 20([0-9])^2
    in_path is a complete path from intro courses to focus requirements"""
    # writes out the in_path to a temp file and then initializes a course graph using that temp file
    # After this, add courses with no prereqs, i.e. course.get_prereqs contains an empty set (this is where completed_courses comes in). This is not enough
    # add those courses to completed_courses
    # and then print
    # I should probably add a helper function to deal with the dict
    with open('.schedule_in_path.csv', 'w') as temp_file:
        writer = csv.writer(temp_file, delimiter=';')
        writer.writerow(['code','name','pre-requisites'])
        for course in in_path:
            prereqs = []
            for prereq_set in course.prereqs:

                for prereq in prereq_set:
                    if prereq in in_path:
                        return
                # if all(prereq in in_path for prereq in prereq_set):
                #     prereqs.append(prereq_set)
            if prereqs != []:
                writer.writerow([course.course_code, course.name, [prereqs]])
            else:
                writer.writerow([course.course_code, course.name, []])
    # def leveler(course: _Course, leveled_dict: dict[_Course: int], curr_level: int = 0):
    #     for prereq_list in course.get_prereqs():
    #         if all(course in in_path for course in prereq_list):  # the current set is the one used in in_path
    #             for prereq in prereq_list:
    #                 if prereq in leveled_dict and leveled_dict[prereq] <= curr_level:
    #                     leveled_dict[prereq] = curr_level + 1
    #                     leveler(prereq, leveled_dict, curr_level + 1)
    #     nonlocal max_level
    #     if max_level < curr_level:
    #         max_level = curr_level
    #
    # max_level = 0
    # leveled_path = {}
    # for course in in_path:
    #     leveled_path[course] = 0
    # for course in in_path:
    #     leveler(course, leveled_path)
    # curr_semester, curr_year = current_semester.split()
    # course_schedule = {}
    # while max_level != 0:
    #     curr_level = max_level
    #     curr_courses = 0
    #     while curr_courses < max_courses_in_semster:
    #         curr_courses += 1


    # so...uhhh...ignore this block
    # def get_prereqs(input_course: _Course, curr_level: int, visited: set = set()) -> list[set[tuple[int, _Course]]]:
    #     def get_union(greater_set: list[set], smaller_set: list[set]):
    #         total_paths = []
    #         for path in greater_set:
    #             for path1 in smaller_set:
    #                 joined_path = path.union(path1)
    #                 total_paths.append(joined_path)
    #         return total_paths
    #
    #     visited.add(input_course)
    #     if len(input_course.prereqs) == 0:
    #         return [{(curr_level, input_course)}]
    #     paths = [set()]
    #     common_course_found = False
    #     for pre_req_set in input_course.prereqs:
    #         sub_paths = []
    #         for pre_req in pre_req_set:
    #             pre_req_paths = []
    #             if pre_req not in visited:
    #                 pre_req_paths = get_prereqs(pre_req, curr_level + 1, visited)
    #             elif not common_course_found:
    #                 pre_req_paths = [set()]
    #                 common_course_found = True
    #             sub_paths.extend(pre_req_paths)
    #         paths = get_union(paths, sub_paths)
    #     for path in paths:
    #         path.add((curr_level, input_course))
    #     return paths
    #
    # path = copy.deepcopy(in_path)
    # for course in completed_courses: # avoid iteration bugs
    #     if course in path:
    #         path.remove(course)



# Lower func was used for testing.  Just keeping it here for now
# def get_prereqs(input_course: _Course, curr_level: int, visited: set = set()) -> list[set[tuple[int, _Course]]]:
#     def get_union(greater_set: list[set], smaller_set: list[set]):
#         total_paths = []
#         for path in greater_set:
#             for path1 in smaller_set:
#                 joined_path = path.union(path1)
#                 total_paths.append(joined_path)
#         return total_paths
#
#     visited.add(input_course)
#     if len(input_course.prereqs) == 0:
#         return [{(curr_level, input_course)}]
#     paths = [set()]
#     common_course_found = False
#     for pre_req_set in input_course.prereqs:
#         sub_paths = []
#         for pre_req in pre_req_set:
#             pre_req_paths = []
#             if pre_req not in visited:
#                 pre_req_paths = get_prereqs(pre_req, curr_level + 1, visited)
#             elif not common_course_found:
#                 pre_req_paths = [set()]
#                 common_course_found = True
#             sub_paths.extend(pre_req_paths)
#         paths = get_union(paths, sub_paths)
#     for path in paths:
#         path.add((curr_level, input_course))
#     return paths
#
