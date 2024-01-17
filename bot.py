import re
import time
import datetime
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import SessionNotCreatedException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url= "https://www.renthub.in.th/login"
login= "sales@bkk.properties"
password= "Rentit_Bkk#!1"

start_time= datetime.time(7)
end_time= datetime.time(23)

tame= datetime.datetime.now().time()

while(tame >= start_time and tame <= end_time): #if current time is between start and end times
    try:
        browser= webdriver.Chrome()
    except SessionNotCreatedException:
        time.sleep(3)
        continue
    
    browser.get(url)

    try: 
        login_bar= browser.find_element_by_id("user_email")
        password_bar= browser.find_element_by_id("user_password")
    except NoSuchElementException: #might be any case. One I've recognized is if net connection is absent
        print """Error [credential elements]: Could not locate elements. Please check your internet connection \n The bot will restart in 30secs,
        if the problem persists; kindly contact the developer.\n"""
        browser.close()
        time.sleep(30) #wait to try again after 30sec
        continue

    login_bar.send_keys(login)
    password_bar.send_keys(password, Keys.RETURN)

    browser.get("https://www.renthub.in.th/dashboard/condo_listings")
    time.sleep(3) #give time to load scripts
    
    #number of pages to be used for loop
    try:
        iterations = browser.find_element_by_class_name("pagination") #refer to class pagination
    except NoSuchElementException:
        print """Error [pagination]: Site structure has been changed; kindly contact the developer.\n Attempting to restart in 30secs\n"""
        browser.close()
        time.sleep(30)
        continue
    
    iterations = len(iterations.find_elements_by_xpath('.//*'))-2 #get all children of pagination class. count them
    #and subtract 2. This equals to total number of pages. Subtracted 2 because, the children also contain, previous
    #and next page buttons. This solves the problem of requiring to change code whenever number of pages differ
    
    for i in range(0, iterations):
        time.sleep(3) #give time to load page

        #element's'. returns a list. Iterate the list, which is updated at each new page, and click on all webObjects(buttons)
        #on the list. Took xpath of a single element. Multiple elements exist on the same path, so all of them are returned
        
        try:
            renew= browser.find_elements_by_xpath('//*[@class="buttonicon"]/div[4]') #getting all the renew buttons on the page
        except NoSuchElementException:
            print "Error [renew button]: Site structure has been changed; kindly contact the developer.\n Attempting to restart in 30secs\n"
            browser.close()
            time.sleep(30)
            continue
        
        length= len(renew) #length of list

        #click on each webObject(button) in the list
        for index in xrange(length):
            try:
                renew[index].click()
            except StaleElementReferenceException:
                continue

        time.sleep(1)

        next_page= browser.find_element_by_class_name("next_page").click() #after all have been renewed. Go to next page

    time.sleep(3)
    browser.close()

    print "Session complete! Waiting 20 minutes for next session to begin\n"

    time.sleep(1200) #20mins
