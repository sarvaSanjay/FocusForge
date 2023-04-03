"""Module Description
===============================
This Python module is the main module and User Interface for the FocusForge application.

Copyright and Usage Information
===============================
This file is provided under the Mozilla Public License 2.0
This file is Copyright (c) 2023 Raahil Vora, Sarva Sanjay, and Ansh Prasad."""


from tkinter import *
from tkinter import ttk
import csv
from typing import Any

import course_graph
import focus

# creates the main screen to display
root = Tk()
root.geometry("500x600")
root.title("FocusForge")
root.configure(background="#282634")
root.resizable(False, False)
listy = set()


def new_window_tt() -> None:
    """This function will open the Timetable builder page."""

    # creates the timetable frame to display
    window = Toplevel(root)
    window.title("Timetable Builder")
    window.geometry("500x600")
    window.configure(background="#282634")
    window.resizable(False, False)

    # create a label to tell the user where they are
    label_timetable = Label(window, text="Timetable builder", bg="#282634", fg="white", font=("Helvetica", 12))
    label_timetable.place(relx=0.5, rely=0.05, anchor=CENTER)

    # tells user to add their completed course
    label_course = Label(window, text="1. Select completed courses", bg="#282634", fg="white", font=("Helvetica", 11))
    label_course.place(relx=0.5, rely=0.1, anchor=CENTER)

    # shows the courses taken below
    label_course2 = Label(window, text="Courses Taken:", bg="#282634", fg="white", font=("Helvetica", 10))
    label_course2.place(relx=0.5, rely=0.22, anchor=CENTER)

    # create a drop-down menu
    courses = read_csv("course-data.csv")
    dropdown = ttk.Combobox(window, values=courses)
    dropdown.place(relx=0.5, rely=0.16, anchor=CENTER)

    # a button to go back to the main window
    button_close = Button(window, text="Close", width=20, height=3, bg="#282620", fg="white", command=window.destroy)
    button_close.place(relx=0.5, rely=0.9, anchor=CENTER)

    # a button which adds the selected course to the list
    button_add = Button(window, text="Add", width=5, height=2, bg="#282620", fg="white",
                        command=lambda: print_list(dropdown.get(), window=window))
    button_add.place(relx=0.7, rely=0.16, anchor=CENTER)

    # tells the user to select focus
    label_focus = Label(window, text="2. Select Focus", bg="#282634", fg="white", font=("Helvetica", 11))
    label_focus.place(relx=0.5, rely=0.4, anchor=CENTER)

    # a button which adds the selected course to the list
    dropdown1 = ttk.Combobox(window, values=read_give_names(), width=60)
    dropdown1.place(relx=0.5, rely=0.45, anchor=CENTER)

    # tells user to ask how many years left
    label_year = Label(window, text="3. Years of study left:", bg="#282634", fg="white", font=("Helvetica", 11))
    label_year.place(relx=0.5, rely=0.6, anchor=CENTER)

    # Button which generates timetable based on courses taken and focus selected for 1 year left
    button_1 = Button(window, text="1", width=4, height=3, bg="#282620", fg="white",
                      command=lambda: find_all_subjects(dropdown1.get(), listy, 4))
    button_1.place(relx=0.35, rely=0.7, anchor=CENTER)

    # Button which generates timetable based on courses taken and focus selected for 2 years left
    button_2 = Button(window, text="2", width=4, height=3, bg="#282620", fg="white",
                      command=lambda: find_all_subjects(dropdown1.get(), listy, 3))
    button_2.place(relx=0.45, rely=0.7, anchor=CENTER)

    # Button which generates timetable based on courses taken and focus selected for 3 years left
    button_3 = Button(window, text="3", width=4, height=3, bg="#282620", fg="white",
                      command=lambda: find_all_subjects(dropdown1.get(), listy, 2))
    button_3.place(relx=0.55, rely=0.7, anchor=CENTER)

    # Button which generates timetable based on courses taken and focus selected for 4 years left
    button_4 = Button(window, text="4", width=4, height=3, bg="#282620", fg="white",
                      command=lambda: find_all_subjects(dropdown1.get(), listy, 1))
    button_4.place(relx=0.65, rely=0.7, anchor=CENTER)


def print_list(course: str, window: Any) -> None:
    """This function will display the list of courses selected by the drop-down menu."""
    if course != '':
        listy.add(course)
        label_courses = Label(window, text=str(listy), bg="#282634", fg="white", font=("Helvetica", 10))
        label_courses.place(relx=0.5, rely=0.26, anchor=CENTER)


# Title for the page
label = Label(root, text="Welcome to FocusForge", bg="#282634", fg="white", font=("Helvetica", 12))
label.place(relx=0.5, rely=0.07, anchor=CENTER)

# add a button which will open the timetable builder page
button = Button(root, text="Timetable Builder", width=20, height=3, bg="#282620", fg="white", command=new_window_tt, )
button.place(relx=0.5, rely=0.2, anchor=CENTER)

# add an image under everything and scale it down
image = PhotoImage(file="logss.png")
image = image.subsample(2, 2)
label = Label(root, image=image, borderwidth=0)
label.place(relx=0.5, rely=0.5, anchor=CENTER)


def read_csv(csv_file: str) -> list:
    """Read the given csv file and return a list of the first item in each row.
    """
    with open(csv_file, encoding='utf8') as filey:
        csvy = csv.reader(filey, delimiter=';')
        first = True
        courses = []
        for course in csvy:
            if first:
                first = False
            else:
                courses.append(course[0])
    return courses


def read_give_names() -> list:
    """Read the given csv file and return a list of the first item in each row for focus specifically.
    """
    return [stry.name for stry in focus.setup_minimal_focii('focus-data.csv')]


def find_all_subjects(focus_name: str, completed: set, num: int) -> None:
    """This function will generate a timetable based on the courses taken and the focus selected."""

    # determines the path and schedule per semester
    graph = course_graph.Graph()
    completed_course = {graph.courses[course] for course in graph.courses if course in completed}
    courses = [stry for stry in focus.setup_minimal_focii('focus-data.csv') if stry.name == focus_name][0]
    focus.complete_minimal_focus(graph, courses, 'focus-data.csv')
    diff_paths = courses.get_paths(completed_course)
    best_path = diff_paths[0]
    for path in diff_paths:
        if len(path) < len(best_path):
            best_path = path
    subjects_per_sem = course_graph.get_schedule(best_path, completed_course)

    # creates the actual frame to display the window
    window = Toplevel(root)
    window.title("Generate timetable for " + focus_name)
    window.state('zoomed')
    window.configure(background="#282634")

    # creates the base of the table
    tree = ttk.Treeview(window, column=("c1", "c2", "c3"), show='headings', height=100)  # not error
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Year to take")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Semester")
    tree.column("# 3", anchor=CENTER)
    tree.heading("# 3", text="Courses")

    # add each semester to the table by iterating through the list
    i = num
    j = 1
    for year in subjects_per_sem:
        for sub in year:
            if j % 2 == 0:
                sem = 'winter'
            else:
                sem = 'Fall'
            tree.insert("", "end", values=(i, sem, sub.course_code))
        if j % 2 == 0:
            i += 1
        j += 1
    tree.pack()


mainloop()

if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'disable': ['forbidden-IO-function', 'forbidden-top-level-code', 'wildcard-import',
                    'forbidden-global-variables', 'too-many-locals'],
        # these are all disabled becuase of use of tkinter and use of print statements to display.
        'extra-imports': ['course', 'tkinter', 'focus', 'csv', 'course_graph', 'typing'],
        # the names (strs) of imported modules
        'max-line-length': 120
    })
