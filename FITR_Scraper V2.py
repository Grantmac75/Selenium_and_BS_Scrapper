from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd

from config import username, password

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)


def closeButton():
    # click the close button of the side panel
    # closeButton = driver.find_element_by_xpath(
    #    '//*[@id="app"]/div[1]/div/div/div[2]/div/div[3]/div/div[36]/div[1]/div[3]/div/button'
    # )
    driver.find_element_by_xpath("//button[text()='Close']").click()
    # closeButton.click()


def forwardButton():
    fButton = driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/div/div/div[2]/div/div[2]/div/div/div[3]/button/span'
    )
    fButton.click()


# login into webpage
url = "https://app.fitr.training/onboarding/sign_in"

driver.get(url)
time.sleep(5)
driver.find_element_by_id("email").send_keys(username)
driver.find_element_by_id("password").send_keys(password)
driver.find_element_by_class_name("onboarding-main-action").click()
time.sleep(2)
# click "accept" button to close the cookies message
acceptButton = driver.find_element_by_xpath(
    '//*[@id="app"]/div[1]/div/div/div[1]/div[2]/div/div/div[2]/div/button[2]'
)
acceptButton.click()
time.sleep(1)

# clicks the arrow back four times to Oct to June.
for d in range(4):
    previous = driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/div/div/div[2]/div/div[2]/div/div/div[1]/button/span'
    )
    previous.click()


# DF set up
data = {"Date": [], "Program": [], "Session": []}
dailyProgram_df = pd.DataFrame(data)

time.sleep(2)

# Scrapping of website
n = 1

while n <= 4:

    # Identify number of days in the month that have a workout - store in NumDays
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    time.sleep(1)
    numDays = soup.find_all("div", {"class": "day same-month full"})
    numDays = len(numDays)
    num = 1
    # Variable of div location for day of the month
    i = 1
    time.sleep(1)

    while num <= numDays:
        print("n= {0} num= {1} numdays= {2}".format(n, num, numDays))

        same_month = driver.find_element_by_xpath(
            '//*[@id="app"]/div[1]/div/div/div[2]/div/div[3]/div/div[' + str(i) + "]"
        ).get_attribute("class")

        if same_month == "day same-month full":

            try:
                # selects the first day of the month using the div position from a variable and clicks the button
                dayButton = driver.find_element_by_xpath(
                    '//*[@id="app"]/div[1]/div/div/div[2]/div/div[3]/div/div['
                    + str(i)
                    + "]/div[2]"
                )
                dayButton.click()
                time.sleep(3)

                # retrieve the source code with the sidebar and creating a Soup
                htmlday = driver.page_source
                soupday = BeautifulSoup(htmlday, "html.parser")
                time.sleep(1)
                # Extract the date of the workout
                dayDate = soupday.find("div", {"class": "position"}).text
                # Finding the number of workouts for that day
                workouts = soupday.find_all("div", {"class": "section-field__body"})

                # Extracting each of the workouts for the day
                for workout in workouts:
                    # Retrieving the program name
                    program = workout.find("h4").text.strip()
                    # Retrieving the training session
                    session = workout.find("div", {"class": "description"})

                    new_row = {"Date": dayDate, "Program": program, "Session": session}

                    dailyProgram_df = dailyProgram_df.append(new_row, ignore_index=True)

                i = i + 1

                # Close sidetabe
                closeButton()
                time.sleep(2)

            except:
                i = i + 1

            num = num + 1
        else:
            i = i + 1
            print("Skipped")
            # num = num + 1
            # numDays = numDays + 1

    n = n + 1
    # Move to next month
    forwardButton()
    time.sleep(3)

dailyProgram_df.to_excel("FITR_Training_Programs.xlsx")
