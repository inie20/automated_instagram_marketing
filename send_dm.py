import random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pickle
import pandas as pd
import logging
import sys
import datetime


#Current Time for logging purposes
current_time = datetime.datetime.now()
current_time_string = current_time.strftime("%Y%m%d_%H%M%S")

#Logger to store terminal responses in a file
file_handler = logging.FileHandler(
    filename=r'C:\Users\indra\PycharmProjects\Quasara_AI\send_dms_' + current_time_string +'.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger('LOGGER_NAME')


# Create a web driver object
logging.info('Creating WebDriver Object')
driver = webdriver.Chrome()


# Authorization or Log In
def log_in(my_username, my_password):
    try:
        logging.info('Loading HomePage')
        driver.get('https://www.instagram.com')
        time.sleep(2)

        try:
            # Click on Accept All Cookies
            logging.info('Clicking Accept All Cookies')
            allow_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button'))
            )
            allow_button.click()

        except:
            # In case there is no cookie banner
            pass

        logging.info('Inputting Credentials')
        # Get to username and password element
        input_username = driver.find_element(By.NAME, "username")
        input_password = driver.find_element(By.NAME, "password")

        input_username.send_keys(my_username)
        time.sleep(1)
        input_password.send_keys(my_password)
        time.sleep(1)
        input_password.send_keys(Keys.ENTER)
        logging.info('Logged In')

        # Wait for the login process to complete
        time.sleep(5)
        logging.info('Saving Cookies')

        # Save the session cookies
        pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

    except Exception as err:
        logging.info(err)
        driver.quit()

#To ensure I only send messages to new users
def has_chatted_before():
    try:
        # Find all elements with attribute role="row"
        row_elements = driver.find_elements(By.CSS_SELECTOR, '[role="row"]')

        # Check if any row element is found
        if len(row_elements) > 0:
            return True
        else:
            return False

    except NoSuchElementException:
        # Handle the case where the element is not found (user has not been messaged before)
        return False


def get_list_usernames(excel_sheet, start_row, number_of_dms):
    try:
        end_row = start_row + number_of_dms
        logging.info('Reading Excel File as DF')
        df=pd.read_excel(excel_sheet)
        logging.info('Reading DF as list of usernames wanted')
        relevant_usernames = df.iloc[start_row:end_row, 0].tolist()
        logging.info('Usernames Extracted')
        return relevant_usernames, end_row
    except Exception as err:
        logging.info(err)

def send_dms(relevant_usernames, message):
    for user in relevant_usernames:
        logging.info(user)

        try:
            #Loading Inbox
            driver.get('https://www.instagram.com/direct/inbox/')
            time.sleep(2)
            # Load saved cookies to maintain the session
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)
            # Refresh the page to apply the loaded cookies
            driver.refresh()
            time.sleep(5)  # Adjust the sleep duration as needed
            # For the Turn on Notifications Dialog
            try:
                button = driver.find_element(By.XPATH, "//button[text()='Not Now']")
                button.click()
            except:
                # In case dialog doesn't show up
                pass
            time.sleep(5)
            # Finding username through search box query
            dm_button = driver.find_element(By.XPATH, "//div[text()='Send message']")
            dm_button.click()
            time.sleep(5)
            #Look for search bar
            search_bar = driver.find_element(By.NAME, "queryBox")
            #Type in Follower Name
            search_bar.send_keys(user)
            time.sleep(random.randrange(4, 6))
            #Select on Correct User
            span_element = driver.find_element(By.XPATH, f"//span[text()='{user}']")
            span_element.click()
            time.sleep(random.randrange(4, 6))
            #Proceed to chat box with user
            chat_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Chat')]")
            chat_element.click()
            time.sleep(5)
            if has_chatted_before():
                logging.info(f'We have chatted with {user} before. Skipping the message. Next User')
            else:
                # Sending the message
                time.sleep(5)
                message_element = driver.find_element(By.XPATH, "//div[@aria-label='Message']")
                # Type Message
                message_element.send_keys(message)
                message_element.send_keys(Keys.ENTER)
                time.sleep(1)
                logging.info(f'{user} Complete! Next User')

        except Exception as err:
            logging.info(err)
            driver.quit()

#Example List to Spam Myself Instead of Others
example_username = ['inie_20']
def main():
    logging.info('Starting Main')
    #Userinput variables
    start_row = int(input("Enter the start row index: "))
    number_of_dms = int(input("Enter the number of DMs to send: "))
    comp_username = str(input('Enter Competitor Username: '))
    # Username and password of my Instagram account
    logging.info('Defining Variables')
    my_username = 'inie_200'
    my_password = 'd_pMz=X2&KaenW9'
    # Excel Sheet
    excel_sheet = f'followers_{comp_username}.xlsx'
    # Message
    message = 'Hello Bois'
    #Begin Function
    logging.info('Function Get Username List Start')
    relevant_usernames,end_row = get_list_usernames(excel_sheet,start_row,number_of_dms)
    logging.info(relevant_usernames)
    logging.info('Function Get Username List End')
    logging.info('Function Log_In Start')
    log_in(my_username,my_password)
    logging.info('Function Log_In End')
    logging.info('Function Send DM start')
    #Using example username to not spam random people. Originally we use relevant_usernames, the list returned from the function get_list_user_names
    send_dms(example_username,message)
    logging.info('Function Send DM end')
    logging.info(f'Last Index for Next Run {end_row} with {comp_username}')
    logging.info('Main Complete')

if __name__ == '__main__':
    main()


#Quit
driver.quit()
