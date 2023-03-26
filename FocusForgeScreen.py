"""This is the Tkinter file for the FocusForge application."""
import csv
from tkinter import *
from tkinter import ttk


class page_1:
    """ This class will create a page 1. """
    # set page 1 as the default page
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()

        # set up the GUI
        self.label = Label(self.frame, text="Welcome to FocusForge")
        self.label.pack()

        self.button = Button(self.frame, text="Timetable Builder", command=self.go_to_page_2)
        self.button.pack()

        # add a button to go to page 3
        self.button = Button(self.frame, text="Focus Selector", command=self.go_to_page_3)
        self.button.pack()

    def go_to_page_2(self):
        """ This function will go to page 2."""
        self.frame.destroy()
        page_2(self.master)

    # add a function to go to page 3
    def go_to_page_3(self):
        """ This function will go to page 3."""
        self.frame.destroy()
        page_3(self.master)


class page_2:
    """ This class will create a page 2. """
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()

        # set up the GUI
        self.label = Label(self.frame, text="Timetable Builder")
        self.label.pack()

        self.button = Button(self.frame, text="Home Screen", command=self.go_to_page_1)
        self.button.pack()

        # add a button to go to page 3
        self.button = Button(self.frame, text="Focus Selector", command=self.go_to_page_3)
        self.button.pack()

        # create a drop-down menu where you can select multiple options
        self.create_dropdown()

        # display all the selections selected by the drop-down menu
        # self.display_selections()

        self.button = Button(self.frame, text="Add subject", command=self.show_list)
        self.button.pack()

        # create a list to store all selections in drop down menu
        self.listy = set()

    def go_to_page_1(self):
        """ This function will go to page 1."""
        self.frame.destroy()
        page_1(self.master)

    def go_to_page_3(self):
        """ This function will go to page 3."""
        self.frame.destroy()
        page_3(self.master)

    # create a drop-down menu where you can select multiple options
    def create_dropdown(self):
        """This function will create a drop-down menu where you can select multiple options."""
        self.dropdown = ttk.Combobox(self.frame, values=self.read_packet_csv(), state="readonly")
        self.dropdown.pack()
        # store and display all selections from drop-down menu with every click
        # self.dropdown.bind("<<ComboboxSelected>>", self.display_selections)

    # display all the selections selected by the drop-down menu
    # def display_selections(self, event=None):
    #     """This function will display the selections made in the drop-down menu."""
    #     self.selections = self.dropdown.get()
    #     self.label = Label(self.frame, text=self.selections)
    #     self.label.pack()

    def show_list(self):
        """This function will show the list of all selections made in the drop-down menu."""
        # IMPORTANT: THIS WILL CHANGE FOR WHEN I GET THE FUNCTIONS TO WORK WITH
        self.selections = self.dropdown.get()
        self.listy.add(self.selections)
        self.label = Label(self.frame, text=str(self.listy))
        self.label.pack()

    def read_packet_csv(self) -> list:
        """Read the given csv file and return a list of the first item in each row.
        """
        with open("data/Bookyums.csv") as filey:
            csvy = csv.reader(filey)
            first = True
            packets = []
            for network in csvy:
                if first:
                    first = False
                else:
                    packets.append(network[0])
        return packets


class page_3:
    """This is the page that will be shown when the user clicks the button to go to Focus Selector."""
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()

        # set up the GUI
        self.label = Label(self.frame, text="Focus Selector")
        self.label.pack()

        self.button = Button(self.frame, text="Home Screen", command=self.go_to_page_1)
        self.button.pack()

        # add a button to go to page 2
        self.button = Button(self.frame, text="Timetable builder", command=self.go_to_page_2)
        self.button.pack()

    def go_to_page_1(self):
        """This function will destroy the current frame and show the page 1 frame."""
        self.frame.destroy()
        page_1(self.master)

    def go_to_page_2(self):
        """This function will destroy the current frame and show the page 2 frame."""
        self.frame.destroy()
        page_2(self.master)


# show page
def show_page():
    """This function will show the page 1 frame as main"""
    root = Tk()
    root.title("FocusForge")
    root.geometry("600x400")
    app = page_1(root)
    root.mainloop()


if __name__ == "__main__":
    show_page()
