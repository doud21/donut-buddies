from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.font as font
from tkmacosx  import Button
import pandas as pd
import random
from tabulate import tabulate as tb
from time import sleep
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#generating GUI for user input
main = Tk()
main.geometry("500x300")

header = font.Font(size=24)
warningdisplay = font.Font(slant="italic")

title = Label(main, text="Donut Buddies Facebook Assignment Bot")
title['font'] = header
warning = Label(main, text="warning: only works with an even amount of group members")
warning['font'] = warningdisplay

email_lab = Label(main, text="Facebook Email")
email_in = Entry(main)

password_lab = Label(main, text="Facebook Password")
password_in = Entry(main)
password_in.config(show="*")

group_lab = Label(main, text="Facebook Group URL")
group_in = Entry(main)

def get_data():
    global data
    path = askopenfilename()
    data = pd.read_csv(path)

csv = Button(main, text="Upload a one or two-column CSV file of names", background="white", command=get_data)

def data_to_post():
    #errors if fields are empty
    if not email_in.get() or not password_in.get() or not group_in.get() or not 'data' in globals():
        message = "ERROR: "
        if not email_in.get():
            message += "Email"
        if not password_in.get():
            if not message:
                message += "Password"
            else:
                message += ", password"
        if not group_in.get():
            if not message:
                message += "Group URL"
            else:
                message += ", group URL"
        if not 'data' in globals():
            if not message:
                message += "CSV file upload"
            else:
                message += ", CSV file upload"
        message += " required."
        print(message)
        return

    #main function
    email = str(email_in.get())
    password = str(password_in.get())
    group = str(group_in.get())

    #reading csv file
    volunteers = data.iloc[:,0].tolist()
    core =  []
    if len(data.columns) == 2:
        core = data.iloc[:,1].tolist()

    #errors if #group members is odd
    if len(core) + len(volunteers) % 2 != 0:
        print("Please upload a CSV with an even amount of members.")
        return

    #randomize function
    def randomize(lst):
        randomized_item = random.randrange(0, len(lst))
        return lst.pop(randomized_item)

    pairs = []

    #pairing core with volunteers
    while len(core) > 0:
        pair = []
        r1 = randomize(core)
        if pd.isnull(r1):
            continue
        r2 = randomize(volunteers)
        pair.append(r1)
        pair.append(r2)
        pairs.append(pair)

    #pairing remaining volunteers with each other
    while len(volunteers) > 0:
        pair = []
        r1 = randomize(volunteers)
        r2 = randomize(volunteers)
        pair.append(r1)
        pair.append(r2)
        pairs.append(pair)

    #construct table string
    table = tb(pairs)
    d = date.today()
    message = 'Pairings for week of ' + d.strftime("%m/%d") + ": \n" + table

    #post to facebook group
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_experimental_option("prefs", { \
    	"profile.default_content_setting_values.notifications": 2 # 1:allow, 2:block
    })

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.facebook.com')

    elem = driver.find_element_by_id('email')
    elem.send_keys(email)
    elem = driver.find_element_by_id('pass')
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)

    driver.maximize_window()
    driver.implicitly_wait(5)

    driver.get(group)

    post_box = driver.find_element_by_xpath("//*[@id='mount_0_0']/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[4]/div/div/div/div/div[1]/div[1]/div/div/div/div[1]/div")
    post_box.click()
    post_box = driver.find_element_by_xpath("//*[@id='mount_0_0']/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div[1]/div[2]/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div/div/div/div")
    post_box.send_keys(message)

    post_button = driver.find_element_by_xpath("//*[@id='mount_0_0']/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div[1]/div[3]/div[2]/div[1]")

    post_button.click()
    sleep(5)

submit = Button(main, text="Generate pairings", bg='#0066CC', fg='white', command=data_to_post)


#Displaying GUI
title.pack()
warning.pack()
email_lab.pack()
email_in.pack()
password_lab.pack()
password_in.pack()
group_lab.pack()
group_in.pack()
csv.pack()
submit.pack(side=BOTTOM)

main.mainloop()
