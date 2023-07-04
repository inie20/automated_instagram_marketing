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

file_handler = logging.FileHandler(
    filename=r'C:\Users\indra\PycharmProjects\Quasara_AI\get_follower_list_' + current_time_string + '.log')
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


def get_follower_list(comp_username):
    try:
        logging.info('Entering Competitors Page')
        # Go to the competitor's followers page
        url_full = f'https://www.instagram.com/{comp_username}/followers/'
        driver.get(url_full)
        logging.info('Loading Cookies into Page')
        # Load saved cookies to maintain the session
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        # Refresh the page to apply the loaded cookies
        driver.refresh()
        time.sleep(10)  # Adjust the sleep duration as needed
        logging.info('Identifying Follower div')
        # Find Element where we have follower information , '_aano' is the name of the class with this data
        div_element = driver.find_element(By.CLASS_NAME, '_aano')
        logging.info('Scrolling through entire Follower List')
        # Scroll the div element to the bottom
        last_height = driver.execute_script('return document.querySelector("div._aano").scrollHeight;')
        while True:
            driver.execute_script('''
                var element = document.querySelector('div._aano');
                element.scrollTop = element.scrollHeight;
            ''')
            time.sleep(5)  # Adjust the sleep duration as needed
            new_height = driver.execute_script('return document.querySelector("div._aano").scrollHeight;')
            if new_height == last_height:
                break
            last_height = new_height
        logging.info('Scrolling Complete')
        logging.info('Finding all links in div')
        anchor_elements = div_element.find_elements(By.TAG_NAME, 'a')
        logging.info('Storing Values in a List')
        # Store href values in a list and use set to remove duplicates
        href_list = list(set([anchor.get_attribute('href') for anchor in anchor_elements]))
        logging.info(href_list)
        logging.info('Duplicates Removed and List Saved')
        # Remove the url format of href_list and store only usernames
        logging.info('Creating List of Cleaned Extracted Data with only username')
        username_list = []

        for href in href_list:
            # Remove the leading 'https://www.instagram.com/' from the URL
            username = href.replace('https://www.instagram.com/', '')

            # Remove the trailing slash '/'
            username = username.rstrip('/')

            username_list.append(username)
            logging.info(username)
        logging.info('Username List Done')
        logging.info(username_list)
        # Create a DataFrame from the list
        logging.info('Saving List as DF')
        #Add new column to identify competitor
        df = pd.DataFrame(username_list, columns=['Username'])
        df['Competitor'] = comp_username
        #Save as an excel file
        logging.info('Saving as Excel')
        df.to_excel(f'followers_{comp_username}.xlsx', index=False)
        logging.info('Excel Saved')

    except Exception as err:
        #Print Error
        logging.info(err)
        driver.quit()


def main():
    logging.info('Starting Main')
    # Username and password of my Instagram account
    logging.info('Defining Credentials')
    my_username = 'inie_200'
    my_password = 'd_pMz=X2&KaenW9'
    # Competitor's Instagram username
    comp_username = str(input('Enter Competitors username: '))
    logging.info('Function Log_In Start')
    log_in(my_username, my_password)
    logging.info('Function Log_In End')
    logging.info('Function Get Follower List Start')
    get_follower_list(comp_username)
    logging.info('Function Get Follower List End')
    logging.info('Main Complete')

if __name__ == '__main__':
    main()
# Close
driver.quit()
