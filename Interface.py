import tkinter as tk
from tkinter import ttk             ## For Input Interface
import re                           ## For Regular Expressions
from BookAccomodation.Book import Book
import BookAccomodation.ConstantData as constants

class AppInterface(tk.Tk):                                                   ## GUI Interface Class

    def __init__(self):
        super().__init__()
        self.title("Booking Bot")
        self.error = False
        self.create_form()

    def create_form(self):
        # Configure Grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)

        # Configure Canvas
        self.geometry("520x280")
        self.resizable(0,0)

        # Error String: To Print Validation Errors
        self.label_error = ttk.Label(self, foreground='red')
        self.label_error.grid(row=0, column=1, sticky=tk.W, padx=5)

        ## Validations
        vfromdate = (self.register(self.validate_from_date),  '%P')
        vtodate   = (self.register(self.validate_to_date),  '%P')
        vloc      = (self.register(self.validate_loc),   '%P')
        vadult    = (self.register(self.validate_adult), '%P')
        vroom     = (self.register(self.validate_room),  '%P')
        # vstar     = (self.register(self.validate_star),  '%P')
        vreview   = (self.register(self.validate_review),'%P')

        # Location Entry
        ttk.Label(text="Location").grid(column=0, row=1, sticky=tk.E, padx=1, pady=5)

        self.loc = ttk.Entry(self, width=45)
        self.loc.config(validate='focusout', validatecommand=vloc)
        self.loc.grid(column=1, row=1, sticky=tk.W, padx=10, pady=5)

        #From Date Entry
        ttk.Label(text="From Date").grid(column=0, row=2, sticky=tk.E, padx=1, pady=5)
        self.label_fromdatehelp = ttk.Label(self, text="(ccyy-mm-dd)", foreground='red')
        self.label_fromdatehelp.grid(column=2, row=2, sticky=tk.E, padx=0, pady=0)

        self.from_date = ttk.Entry(self, width=30)
        self.from_date.config(validate='focusout', validatecommand=vfromdate)
        self.from_date.grid(column=1, row=2, sticky=tk.W, padx=10, pady=5)

        #To Date Entry
        ttk.Label(text="To Date").grid(column=0, row=3, sticky=tk.E, padx=1, pady=5)
        self.label_todatehelp = ttk.Label(self, text="(ccyy-mm-dd)", foreground='red')
        self.label_todatehelp.grid(column=2, row=3, sticky=tk.E, padx=0, pady=0)

        self.to_date = ttk.Entry(self, width=30)
        self.to_date.config(validate='focusout', validatecommand=vtodate)
        self.to_date.grid(column=1, row=3, sticky=tk.W, padx=10, pady=5)

        # Adults
        ttk.Label(text="Adults").grid(column=0, row=4, sticky=tk.E, padx=1, pady=5)

        self.adults = ttk.Entry(width=15)
        self.adults.config(validate='focusout', validatecommand=vadult)
        self.adults.grid(column=1, row=4, sticky=tk.W, padx=10, pady=5)

        # Rooms
        ttk.Label(text="Rooms").grid(column=0, row=5, sticky=tk.E, padx=1, pady=5)

        self.rooms = ttk.Entry(width=15)
        self.rooms.config(validate='focusout', validatecommand=vroom)
        self.rooms.grid(column=1, row=5, sticky=tk.W, padx=10, pady=5)

        # #star
        # ttk.Label(text="Star Rating").grid(column=0, row=6, sticky=tk.E, padx=1, pady=5)
        #
        # self.star = ttk.Entry(width=15)
        # self.star.config(validate='focusout', validatecommand=vstar)
        # self.star.grid(column=1, row=6, sticky=tk.W, padx=10, pady=5)

        #Review Rating
        ttk.Label(text="Review Rating").grid(column=0, row=6, sticky=tk.E, padx=0, pady=5)

        self.review = ttk.Entry(width=15)
        self.review.config(validate='focusout', validatecommand=vreview)
        self.review.grid(column=1, row=6, sticky=tk.W, padx=10, pady=5)

        #Buttons
        self.bot_button   = ttk.Button(text='Run Bot', command = self.runbot).grid(row=9, column=0, padx=5, pady=30)
        self.close_button = ttk.Button(text='Close', command = self.quitApp).grid(row=9, column=3, padx=5, pady=30)

    def runbot(self):
        self.label_error.setvar("")
        if self.error or self.loc.get() == "" or self.from_date.get() == "" or self.to_date.get() == "" or \
            self.adults.get() == "" or self.rooms.get() == "" or self.review.get() == "":
            self.show_message("Inputs are Not Correct / Missing")
        else:
            with Book(teardown=True) as bookbot:               ## Perform Scraping Selection Actions
                    bookbot.initial_site()
                    bookbot.select_country()
                    bookbot.change_country()
                    bookbot.select_currency()
                    bookbot.change_currency(currency=constants.CURRENCY_TYPE)
                    bookbot.select_location(self.loc.get().strip())
                    bookbot.select_period(checkin_date=self.from_date.get().strip(), checkout_date=self.to_date.get().strip())
                    bookbot.select_guest_details(adults=int(self.adults.get().strip()), rooms=int(self.rooms.get().strip()))
                    bookbot.click_search()                          ## Start Search
                    bookbot.getdata(self.review.get().strip())                               ## Scrape Data from Top(25) Cards
    def quitApp(self):
        exit()

    def validate_adult(self, value):                            ## Validate Adult Count Input
        self.error = False

        if value == None or value == '':
            self.show_message(f"Invalid Adult Count *{value}*")
            self.error = True
            return False

        if int(value) > 30 or int(value) < 1:                 ## Validate Range
            self.show_message(f"Invalid Adult Count {value}")
            self.error = True
            return False

        self.show_message("")
        return True

    def validate_room(self, value):                            ## Validate Room Count Input
        self.error = False

        if value == None or value == '':
            self.show_message(f"Invalid Room Count *{value}*")
            self.error = True
            return False

        if int(value) > 10 or int(value) < 1:                 ## Validate Range
            self.show_message(f"Invalid Room Count {value}")
            self.error = True
            return False

        self.show_message("")
        return True

    # def validate_star(self, value):
    #         list = value.split(",")
    #         flag = True
    #         self.error = False
    #
    #         if value == '':
    #             self.show_message(f"Invalid Star Rating {value}")
    #             self.error = True
    #             return False
    #
    #         for star in list:
    #             if star == None or star == '':
    #                 flag=False
    #
    #             if int(star.strip()) < 0 or int(star.strip()) > 5:
    #                 flag=False
    #
    #         if flag==False:
    #             self.show_message(f"Invalid Star Rating {value}")
    #             self.error = True
    #             return False
    #
    #         self.show_message("")
    #         return True

    def validate_review(self, value):    ## Validate Review Rating: Can be Used In Post Filteration,not filtered during scraping
        self.error = False

        if value == None or value == '':
            self.show_message(f"Invalid Review Value *{value}*")
            self.error = True
            return False

        if float(value) > 10.0 or float(value) < 1.0:                           ## Validate Review Rating Range Input
            self.show_message(f"Invalid Review Value {value}")
            self.error = True
            return False

        self.show_message("")
        return True

    def validate_loc(self, loc):                                       ## Validate Location Input
        self.error = False

        if loc == None or loc == '':
            self.show_message(f"Invalid Location *{loc}*")
            self.error = True
            return False

        if len(loc.strip()) < 5:
            self.show_message("Invalid Location")
            self.error = True
            return False

        self.show_message("")
        return True

    def check_date(self, value):                                ## Check Date using Regular Expression
        pattern = r'^202[2-9]-[0-1][0-9]-[0-3][0-9]$'
        if re.fullmatch(pattern, value) is None:
            self.show_message("Invalid Date")
            return False
        return True

    def validate_from_date(self, value):                        ## Validate From Date Input
        self.error = False
        if self.check_date(value) == False:
            self.error = True
            return False

        self.show_message("")
        return True

    def validate_to_date(self, value):                          ## Validate To Date Input
        self.error = False
        if self.check_date(value) == False:
            self.error = True
            return False

        self.show_message("")
        return True

    def show_message(self, error='', color='black'):            ## Method to Display Error Message on GUI
        self.label_error['text'] = error
        self.from_date['foreground'] = color

