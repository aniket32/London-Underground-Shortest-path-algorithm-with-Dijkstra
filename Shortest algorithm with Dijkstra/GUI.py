# Created by Ian Louzada
from tkinter import messagebox
from tkinter import *
import csv
import os
import main


def close_win():
    """Close the GUI window"""
    root.destroy()


class UIInterface:
    def __init__(self, win):
        self.start_Station = ''
        self.end_Station = ''
        self.win = win
        self.win.title("Journey Planner")
        self.win.geometry("900x700")
        self.win.resizable(width=0, height=0)
        self.img = PhotoImage(file="back.png")
        self.label = Label(self.win, image=self.img)
        self.label.image = self.img
        self.label.pack()

        self.select_menu()

    def select_menu(self):

        # Plan Journey Button Specification, Commands and Placing
        self.button1 = Button(self.win, text="Plan Journey", bg="white", height=2, width=30, command=self.check_time_correct)
        self.button1.place(x=300, y=400)

        # Time Title Box Specification and Placing
        self.time_title = Label(self.win, text="What time are you leaving?", height=1, width=21)
        self.time_title.place(x=50, y=150)

        # Hour Entry Box Specification and Placing
        self.time_entry = Entry(self.win, bg="white", width=5)
        self.time_entry.place(x=65, y=200)

        # Minute Entry Box Specification and Placing
        self.time_entry2 = Entry(self.win, bg="white", width=5)
        self.time_entry2.place(x=105, y=200)
        # # Time Check Box Specification, Command and Placing

        # Exit Button Specification, Commands and Placing
        self.exit_button = Button(self.win, text="Exit", bg="white", height=2, width=10, command=self.exit_warning)
        self.exit_button.place(x=75, y=600)

        # Station name List Box Specification and Placing
        self.menu1 = Listbox(self.win, width=30, height=10)
        self.menu1.place(x=320, y=200)

        # Start Destination Button Specification, Commands and Placing
        self.start_button = Button(self.win, text="Start Destination", bg="white", height=1, width=15,
                                   command=self.set_Start)
        self.start_button.place(x=185, y=250)

        # End Destination Button Specification, Commands and Placing
        self.end_button = Button(self.win, text="End Destination", bg="white", height=1, width=15, command=self.set_End)
        self.end_button.place(x=530, y=250)

        # Search Label for Stations name Specification and Placing
        self.search_var = StringVar()
        self.search_var.trace("w", self.update_list)
        self.entry = Entry(self.win, textvariable=self.search_var, width=30, highlightthickness=5,
                           highlightcolor='black')
        self.entry.place(x=315, y=150)

        # Route Display Specification and Placing
        self.routeLabel = Label(self.win, text="", width=50, bg='white')
        self.routeLabel.place(x=240, y=375)

        # Refresh Page Button Specification, Commands and Placing
        self.refresh_button = Button(self.win, text="Refresh", bg="white", height=2, width=10, command=self.refresh)
        self.refresh_button.place(x=700, y=600)

        # Calling the function to change the Route Destinations as selected in the interface
        self.update_list()

    def selection(self):
        """ Checking if the Start and End Stations are same or not and executes the run function for table results"""
        if self.start_Station == self.end_Station:
            self.error_msg()
        else:
            main.run(self.start_Station, self.end_Station, self.check_time())


    def exit_warning(self):
        """Message Box to confirm or cancel exiting the interface"""
        res = messagebox.askyesno("Exit Message", "Do you want to Quit?")
        if res == TRUE:
            close_win()
        else:
            self.select_menu()

    def get_hour(self):
        """Return the time variable in the hours box"""
        self.hour = self.time_entry.get()
        return self.hour

    def get_min(self):
        """Return the time variable in the minutes box"""
        self.min = self.time_entry2.get()
        return self.min

    def check_time_correct(self):
        """Check if the time entered is valid and in the correct format"""
        if self.get_hour() == '' or self.get_min() == '' or len(str(self.get_hour())+str(self.get_min())) != 4:
            messagebox.showerror("Ok", "Please enter a valid time. Use the format HH:MM")
            self.refresh()
        else:
            if int(self.get_hour()) >= 24 or int(self.get_min()) > 59:
                messagebox.showerror("Ok", "Please enter a valid time. Use the format HH:MM")
                self.refresh()
            else:
                self.selection()

    def check_time(self):
        """Return the time entered as an int"""
        return int(str(self.get_hour())+str(self.get_min()))

    def refresh(self):
        """Closing and reopening the interface to justify any errors or start a new"""
        close_win()
        os.system('main.py')

    def get_start(self):
        """Grabs the selected start destination from the List of Stations"""
        self.start = self.menu1.get(ACTIVE)
        return self.start

    def get_end(self):
        """Grabs the selected end destination from the List of Stations"""
        self.end = self.menu1.get(ACTIVE)
        return self.end

    def set_Start(self):
        """Updating the route start destination as selected"""
        self.start_Station = self.get_start()

        if self.end_Station != '':
            updatedText = "From %s to %s" % (self.start_Station, self.end_Station)
        else:
            updatedText = "From %s" % self.start_Station
        self.routeLabel.config(text=updatedText)

    def set_End(self):
        """Updating the route end destination as selected"""
        self.end_Station = self.get_end()

        if self.start_Station != '':
            updatedText = "From %s to %s" % (self.start_Station, self.end_Station)
        else:
            updatedText = "%s to %s" % (self.routeLabel['text'], self.end_Station)

        self.routeLabel.config(text=updatedText)

    def update_list(self, *args):
        """Filling the List Box with names of Station as well as checking for the search term and showing relevant
        results """
        search_term = self.search_var.get()
        self.file = open("Station List Data.csv")
        self.reader = csv.reader(self.file)
        self.data = list(self.reader)

        station_lst = []
        for x in list(range(1, len(self.data))):
            station_lst.append(self.data[x][0])  # Appends data to list
        menu1 = station_lst

        self.menu1.delete(0, END)

        for item in menu1:
            if search_term.lower() in item.lower():
                self.menu1.insert(END, item)

    def error_msg(self):
        """Message Box to confirm that the destinations fields are either empty or same"""
        messagebox.showerror("Ok", "The Start and the End Destination are same or not specified")
        self.select_menu()


def route_not_possible():
    """Message Box to confirm that the Route selected cannot be Traversed"""
    messagebox.showerror("Retry", "The Selected Route is not possible, Please Click on Refresh to Continue")


def results(data, time):
    """TopLevel tkinter window to show the Journey Summary and also the total time"""
    root2 = Toplevel()
    root2.title("Your Journey")
    root2.resizable(True, True)
    root2.geometry("+550+300")

    # Table Code
    # Added a parameter to this method for get the info
    col = 3
    rows = len(data)

    for i in range(rows):
        for j in range(col):
            b = Label(root2, font=("system", 12, 'bold'), bg="black", fg="orange", width=35, text=data[i][j])
            b.grid(row=i, column=j)

    total = Label(root2, font=("system", 12, 'bold'), bg="black", fg="orange", width=35,
                  text=" Total Time(in mins) = " + str(time))
    total.grid()

    exit_button = Button(text="Exit", bg="white", height=2, width=10, command=quit)
    exit_button.place()


root = Tk()
my_gui = UIInterface(root)
root.mainloop()
