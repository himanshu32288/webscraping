import numpy as np
from selenium import webdriver as WD
import os as OS
import BookAccomodation.ConstantData as constants
from selenium.webdriver.common.by import By

class Book(WD.Chrome): 
    def __init__(self, wd_path=constants.DRIVER_PATH, teardown=False):  ## Constructor
        self.wd_path = wd_path  ## Set Environment Path for Webdriver
        self.teardown = teardown  ## Flag to call destructor
        OS.environ['PATH'] += self.wd_path
        options = WD.ChromeOptions()                                    ## Suppress Warnings on Console Run
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Book, self).__init__(options=options)                     ## Instantiate parent class: webdriver
        self.implicitly_wait(constants.IMPLICIT_WAIT)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):  ## Destructor
        if self.teardown:
            self.quit()                                                 ## Close Chrome Browser

    def initial_site(self):  ## Open Website
        self.get(constants.BOOKING_URL)

    def select_country(self):  ## Click Country / Language button
        try:
            self.find_element(By.CSS_SELECTOR, "button[data-tooltip-text='Choose your language']").click()
        except:
            print("Unable to Get Country")

    def change_country(self):  ## Select Country / Language
        try:
            self.find_element(By.CSS_SELECTOR, "div[lang='en-us']").click()  ## May find better element to locate
        except:
            print("Unable to Change Country")

    def select_currency(self):  ## Click Current button
        try:
            self.find_element(By.CSS_SELECTOR, "button[data-tooltip-text='Choose your currency']").click()
            #self.find_element(By.CSS_SELECTOR, "button[aria-describeby='_zec7jz5up']").click()
        except:
            print("Unable to Get Currency")

    def change_currency(self, currency=None):
        try:
            self.find_element(By.CSS_SELECTOR,
                          f"a[data-modal-header-async-url-param*='selected_currency={currency}']").click()
        except:
            print("Unable to Change Currnecy")


    def select_location(self, location):  ## Select City of Visit
        location_box = self.find_element(By.ID, "ss")
        location_box.clear()
        location_box.send_keys(location)

        try:
            first_choice = self.find_element(By.CSS_SELECTOR, "li[data-i='0']")
            first_choice.click()
        except:
            self.close()                                    ## Not input selection. Close program

    def select_period(self, checkin_date, checkout_date):  ## Select Period from Display Calendar
        checkin_date_element = self.find_element(By.CSS_SELECTOR, f"td[data-date='{checkin_date}']")
        checkin_date_element.click()

        checkout_date_element = self.find_element(By.CSS_SELECTOR, f"td[data-date='{checkout_date}']")
        checkout_date_element.click()

    def select_guest_details(self, adults, rooms):  ## Select Adult Count & Required Rooms Count
        guest_element = self.find_element(By.ID, "xp__guests__toggle")  ## Get on to Guest Box Drop down
        guest_element.click()

        while True:  ## Reduce Adults until 1
            reduce_adults = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Decrease number of Adults"]')
            reduce_adults.click()  ## Reduce Adult Count
            adult_count_element = self.find_element(By.ID, "group_adults")
            adult_count = adult_count_element.get_attribute('value')  ## Adult Count

            if adult_count == '1':
                break

        for i in range(0, adults - 1):  ## Increase Adults to desired count
            try:
                increase_adults = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Increase number of Adults"]')
                increase_adults.click()
            except:
                print("ERROR ADDING ADULTS")
                break

        while True:  ## Reduce Rooms until 1
            reduce_rooms = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Decrease number of Rooms"]')
            reduce_rooms.click()  ## Reduce Rooms Count
            rooms_count_element = self.find_element(By.ID, "no_rooms")
            rooms_count = rooms_count_element.get_attribute('value')  ## Room Count Count

            if rooms_count == '1':
                break

        for i in range(0, rooms - 1):  ## Increase Rooms to desired count
            try:
                increase_rooms = self.find_element(By.CSS_SELECTOR,
                                                   'button[aria-label="Increase number of Rooms"]')
                increase_rooms.click()
                print()
            except:
                print("ERROR ADDING ROOMS")
                break

    def click_search(self):  ## Search Based on Selections
        self.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    def normstr(str):   ## Normalize string by stripping and removing special character for Rupee.
        str=str.strip().replace(constants.RUPEE_SYMBOL, "Rs. ")
        return str

    def toCSV(arr, rating):
        with open(constants.OUT_FILE, "w") as fd:
            line = '"Hotel_Name","Hotel_Address","Hotel_Distance","Hotel_Score","Hotel_Price"\n'  ## Header
            fd.write(line)                       ## Print Header To CSV
            for dictrow in arr:
                line=""
                review=0
                for dictelement in dictrow:
                    line = line + '"' + Book.normstr(dictrow[dictelement]) + '",'
                    try:
                        if(dictelement == "Hotel Score"):  ## Set Review Rating for Current Record
                            review = float(Book.normstr(dictrow[dictelement]))
                    except:
                        review = 0.0
                line = line[:-1]
                line=Book.normstr(line)
                try:
                    if(review >= float(rating)):           ## Filter based on Rating of Hotel, Reject if Rating not available
                       fd.write(line+"\n")                 #3 Print Record to CSV
                except:
                    pass

        OS.system("start EXCEL.EXE " + constants.OUT_FILE)

    def getdata(self, rating):  ## Fetch Property Details, Store & Print
        hotel_boxes = self.find_element(By.CLASS_NAME, "d4924c9e74").find_elements(
            By.CSS_SELECTOR, "div[data-testid='property-card']")
        Hotel_List = np.array([])  ## Array to Hold Result (Dictionaries)

        for hotel_card in hotel_boxes:  ## Iterate each Property Card
            ## Initialize Variables
            hotel_name = "HOTEL NAME NOT AVAILABLE"
            hotel_address = "HOTEL ADDRESS NOT AVAILABLE"
            hotel_distance = "HOTEL DISTANCE NOT AVAILABLE"
            hotel_score = "NO SCORE AVAILABLE"
            hotel_review_cnt = "NO REVIEW AVAILABLE"
            hotel_review_comment = "NO REVIEW COMMENT AVAILABLE"
            hotel_spl = "NO LOCATION RATING AVAILABLE"
            hotel_price = "NO PRICE AVAILABLE"

            try:  ## Fetch elements
                try:
                    hotel_name = hotel_card.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').get_attribute(
                        'innerHTML')
                except:
                    print("unable to get Hotel Name")
                try:
                    hotel_address = hotel_card.find_element(By.CSS_SELECTOR,
                                                            'span[data-testid="address"]').get_attribute(
                        'innerHTML')
                except:
                    print("unable to get Hotel Address")
                try:
                    hotel_distance = hotel_card.find_element(By.CSS_SELECTOR,
                                                             'span[data-testid="distance"]').get_attribute(
                        'innerHTML')
                except:
                    print("unable to get Hotel Distance")
                try:
                    hotel_score = hotel_card.find_element(By.CSS_SELECTOR, 'div[aria-label*="Scored"]').get_attribute(
                        'innerHTML')
                except:
                    print("unable to get Hotel Score")
                # try:
                #     hotel_review_cnt = hotel_card.find_element(By.CSS_SELECTOR,
                #            'div[class="d8eab2cf7f c90c0a70d3 db63693c62"]').get_attribute('innerHTML')
                # except:
                #     print("unable to get Hotel Review Count")
                #
                # try:
                #     hotel_review_comment = hotel_card.find_element(By.CSS_SELECTOR,
                #                            'div[class="b5cd09854e f0d4d6a2f5 e46e88563a"]').get_attribute(
                #         'innerHTML')
                # except:
                #     print("unable to get Hotel Review Comment")

                # try:
                #     hotel_spl = hotel_card.find_element(By.CSS_SELECTOR,
                #                                             'span[class="f9afbb0024"]').get_attribute(
                #         'innerHTML')
                # except:
                #     print("unable to get Hotel Special")

                try:
                    hotel_price = hotel_card.find_element(By.CSS_SELECTOR,
                                                          'span[class="fcab3ed991 bd73d13072"]').get_attribute(
                        'innerHTML')
                    hotel_price = hotel_price.replace("&nbsp;", " ")
                except:
                    print("unable to get Hotel Price")

                # dict = {"Hotel Name": hotel_name, "Hotel Address": hotel_address,
                #         "Hotel Distance": hotel_distance, "Hotel Score": hotel_score,
                #        "Hotel Review Count": hotel_review_cnt, "Hotel Review Exclamation": hotel_review_comment,
                #        "Hotel Price": hotel_price
                #        }

                ## Put Result Record to Dictionary
                dict_rec = {"Hotel Name": hotel_name, "Hotel Address": hotel_address, "Hotel Distance": hotel_distance,
                            "Hotel Score": hotel_score, "Hotel Price": hotel_price
                            }

                Hotel_List = np.append(Hotel_List, dict_rec)  ## Append Dictionary Record to Array

            except Exception as e:
                print(e)

        print(Hotel_List)  ## Print Result
        #print(len(Hotel_List))
        Book.toCSV(Hotel_List, rating)
