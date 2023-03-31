"""This is the Tkinter file for the FocusForge application."""
import csv
from tkinter import *
from tkinter import ttk
# from python_ta.contracts import check_contracts

root = Tk()
root.geometry("500x600")
root.title("FocusForge")
root.configure(background="#282634")

# given a list of courses calculates the total credits required for that path
# given a set of courses, choose

# @check_contracts
def new_window_tt():
    """This function will open the Timetable builder page."""
    listy = set()
    window = Toplevel(root)
    window.title("Timetable Builder")
    window.geometry("500x600")
    window.configure(background="#282634")

    # create a label to tell the user where they are
    label = Label(window, text="Timetable builder", bg="#282634", fg="white", font=("Helvetica", 12))
    label.place(relx=0.5, rely=0.1, anchor=CENTER)

    label = Label(window, text="Courses Taken:", bg="#282634", fg="white", font=("Helvetica", 12))
    label.place(relx=0.5, rely=0.45, anchor=CENTER)
    # create a drop-down menu
    courses = read_packet_csv()
    dropdown = ttk.Combobox(window, values=courses, state="readonly")
    dropdown.place(relx=0.5, rely=0.3, anchor=CENTER)

    # a button to go back to the main window
    button = Button(window, text="Close", width=20, height=3, bg="#282620", fg="white", command=window.destroy)
    button.place(relx=0.5, rely=0.9, anchor=CENTER)

    # a button which adds the selected course to the list
    button = Button(window, text="Add", width=20, height=3, bg="#282620", fg="white",
                    command=lambda: print_list(listy, dropdown.get(), window=window))
    button.place(relx=0.5, rely=0.45, anchor=CENTER)

    button = Button(window, text="Generate timetable", width=20, height=3, bg="#282620", fg="white",
                    command=window.destroy)  # TODO: add a function to this button
    button.place(relx=0.5, rely=0.8, anchor=CENTER)


# @check_contracts
def new_window_fs():
    """This function will open the focus selector page."""
    listy = set()
    window = Toplevel(root)
    window.title("Focus Selector")
    window.geometry("500x600")
    window.configure(background="#282634")
    label = Label(window, text="Focus Selector", bg="#282634", fg="white")
    label.place(relx=0.5, rely=0.05, anchor=CENTER)

    # create a drop-down menu where you can select multiple options
    courses = read_packet_csv()
    dropdown = ttk.Combobox(window, values=courses, state="readonly")
    dropdown.place(relx=0.5, rely=0.3, anchor=CENTER)

    # create a button which adds the selected course to the list
    button = Button(window, text="Find Focus", width=20, height=3, bg="#282620", fg="white",
                    command=window.destroy)  # TODO: add a function to this button
    button.place(relx=0.5, rely=0.8, anchor=CENTER)

    label = Label(window, text="Courses Taken/ want to take:", bg="#282634", fg="white", font=("Helvetica", 12))
    label.place(relx=0.5, rely=0.45, anchor=CENTER)

    # a button which adds the selected course to the list
    button = Button(window, text="Add", width=20, height=3, bg="#282620", fg="white",
                    command=lambda: print_list(listy, dropdown.get(), window=window))
    button.place(relx=0.5, rely=0.6, anchor=CENTER)

    # create a button to go back to the main window
    button = Button(window, text="Close", width=20, height=3, bg="#282620", fg="white", command=window.destroy)
    button.place(relx=0.5, rely=0.9, anchor=CENTER)


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
        label.place(relx=0.5, rely=0.5, anchor=CENTER)


label = Label(root, text="Welcome to FocusForge", bg="#282634", fg="white", font=("Helvetica", 12))
label.place(relx=0.5, rely=0.07, anchor=CENTER)

# add a button which will open the timetable builder page
button = Button(root, text="Timetable Builder", width=20, height=3, bg="#282620", fg="white", command=new_window_tt, )
button.place(relx=0.35, rely=0.2, anchor=CENTER)

# add a button which will open the focus selector page
button = Button(root, text="Focus selector", width=20, height=3, bg="#282620", fg="white", command=new_window_fs, )
button.place(relx=0.65, rely=0.2, anchor=CENTER)

# add an image under everything and scale it down
image = PhotoImage(file="logss.png")
image = image.subsample(2, 2)
label = Label(root, image=image, borderwidth=0)
label.place(relx=0.5, rely=0.5, anchor=CENTER)


# @check_contracts
def read_packet_csv() -> list:
    """Read the given csv file and return a list of the first item in each row.
    """
    with open("Bookyums.csv") as filey:
        csvy = csv.reader(filey)
        first = True
        packets = []
        for network in csvy:
            if first:
                first = False
            else:
                packets.append(network[0])
    return packets


mainloop()


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    # import python_ta

    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['E9992', 'E9997']
    # })
