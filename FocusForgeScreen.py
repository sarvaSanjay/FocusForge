
"""This is the Tkinter file for the FocusForge application."""

import csv
import focus
from tkinter import *
from tkinter import ttk
import CourseGraph
# from python_ta.contracts import check_contracts
root = Tk()
root.geometry("500x600")
root.title("FocusForge")
root.configure(background="#282634")

listy = set()
focy = ''

def new_window_compvis():
    window = Toplevel(root)
    window.title("Focus Selector")
    window.geometry("500x600")
    window.configure(background="#282634")
    label = Label(window, text="Focus Selector", bg="#282634", fg="white")
    label.place(relx=0.5, rely=0.05, anchor=CENTER)

    tree = ttk.Treeview(window, column=("c1", "c2", "c3"), show='headings', height=8)
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Year to take")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Fall")
    tree.column("# 3", anchor=CENTER)
    tree.heading("# 3", text="Winter")
    # Insert the data in Treeview widget


# @check_contracts
def new_window_tt():
    """This function will open the Timetable builder page."""

    window = Toplevel(root)
    window.title("Timetable Builder")
    window.geometry("500x600")
    window.configure(background="#282634")

    # create a label to tell the user where they are
    label = Label(window, text="Timetable builder", bg="#282634", fg="white", font=("Helvetica", 12))
    label.place(relx=0.5, rely=0.1, anchor=CENTER)

    label = Label(window, text="Courses Taken:", bg="#282634", fg="white", font=("Helvetica", 12))
    label.place(relx=0.5, rely=0.25, anchor=CENTER)
    # create a drop-down menu
    courses = read_packet_csv("Bookyums.csv")
    dropdown = ttk.Combobox(window, values=courses, state="readonly")
    dropdown.place(relx=0.5, rely=0.2, anchor=CENTER)

    # a button to go back to the main window
    button = Button(window, text="Close", width=20, height=3, bg="#282620", fg="white", command=window.destroy)
    button.place(relx=0.5, rely=0.9, anchor=CENTER)

    # a button which adds the selected course to the list
    button = Button(window, text="Add", width=20, height=2, bg="#282620", fg="white",
                    command= lambda: print_list(listy, dropdown.get(), window=window))
    button.place(relx=0.5, rely=0.35, anchor=CENTER)

    dropdown1 = ttk.Combobox(window, values= read_give_names(), state="readonly")
    dropdown1.place(relx=0.5, rely=0.45, anchor=CENTER)
    button = Button(window, text="Select focus", width=20, height=3, bg="#282620", fg="white",
                    command= lambda: print_focus(dropdown1.get(), window=window))
    button.place(relx=0.5, rely=0.6, anchor=CENTER)


    button = Button(window, text="1", width=4, height=3, bg="#282620", fg="white",
                    command= lambda: find_all_subjects(dropdown1.get(),listy))
    button.place(relx=0.35, rely=0.75, anchor=CENTER)
    button = Button(window, text="2", width=4, height=3, bg="#282620", fg="white",
                    command=lambda: new_window_compvis(dropdown1.get(), 2))
    button.place(relx=0.45, rely=0.75, anchor=CENTER)
    button = Button(window, text="3", width=4, height=3, bg="#282620", fg="white",
                    command=lambda: new_window_compvis(dropdown1.get(), 3))
    button.place(relx=0.55, rely=0.75, anchor=CENTER)
    button = Button(window, text="4", width=4, height=3, bg="#282620", fg="white",
                    command= lambda: new_window_compvis(dropdown1.get(), 4))
    button.place(relx=0.65, rely=0.75, anchor=CENTER)

# @check_contracts
def create_dropdown(window):
    """This function will create a drop-down menu where you can select multiple options."""
    # create a list of all the courses
    courses = read_packet_csv()
    # create a drop-down menu
    dropdown = ttk.Combobox(window, values=courses, state="readonly")
    # move it to bottom
    dropdown.place(relx=0.5, rely=0.3, anchor=CENTER)


# @check_contracts
def print_list(listy, course, window):
    """This function will display the list of courses selected by the drop-down menu."""
    if course != '':
        listy.add(course)
        label = Label(window, text=str(listy), bg="#282634", fg="white", font=("Helvetica", 10))
        label.place(relx=0.5, rely=0.28, anchor=CENTER)

def print_focus(fox: str, window):
    """This function will display the list of courses selected by the drop-down menu."""
    global courses
    if fox != '':
        focy = fox
        label = Label(window, text=str(focy), bg="#282634", fg="white", font=("Helvetica", 10))
        label.place(relx=0.5, rely=0.28, anchor=CENTER)
        print(courses)


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



# @check_contracts
def read_packet_csv(csv_file: str) -> list:
    """Read the given csv file and return a list of the first item in each row.
    """
    with open(csv_file) as filey:
        csvy = csv.reader(filey, delimiter=';')
        first = True
        packets = []
        for network in csvy:
            if first:
                first = False
            else:
                packets.append(network[0])
    return packets

def read_give_names() -> list:
    """Read the given csv file and return a list of the first item in each row.
    """
    return[stry.name for stry in focus.setup_minimal_focii('focus-data.csv')]


def find_all_subjects(focus_name: str, completed: set):
    """yum"""

    graph = CourseGraph.Graph()
    courses = [stry for stry in focus.setup_minimal_focii('focus-data.csv') if stry.name == focus_name][0]
    focus.complete_minimal_focus(graph, courses, 'focus-data.csv')
    diff_paths = courses.get_paths(completed)
    subjects_per_sem = CourseGraph.get_schedule(diff_paths[0], completed)

    window = Toplevel(root)
    window.title("Focus Selector")
    window.geometry("500x600")
    window.configure(background="#282634")
    label = Label(window, text="Focus Selector", bg="#282634", fg="white")
    label.place(relx=0.5, rely=0.05, anchor=CENTER)

    tree = ttk.Treeview(window, column=("c1", "c2", "c3"), show='headings', height=8)
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Year to take")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Semester")
    tree.column("# 3", anchor=CENTER)
    tree.heading("# 3", text="Courses")
    # Insert the data in Treeview widget
    for i in range(1, len(subjects_per_sem)):
        sub_so_far = []
        if i % 2 == 0:
            sem = 'Winter'
        else:
            sem = 'fall'
        for subject in subjects_per_sem[i]:
            sub_so_far.append(subject.course_code)
            print(sub_so_far)
        tree.insert('', 'end', text="1", values=(str(i), sem, str(sub_so_far)))
        i += 1
    tree.pack()

mainloop()

