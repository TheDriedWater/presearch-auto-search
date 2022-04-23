from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
from configuration import config
import os
# import winsound


#  Initialization
words = open("words.txt", "r").readlines()

#  Setting up chrome
user_data_path = 'C:/Users/{}/AppData/Local/Google/Chrome/User Data'.format(os.getlogin())
profile_name = "Profile " + str(config["profile_number"])

options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=' + user_data_path)
options.add_argument('--profile-directory=' + profile_name)
# options.add_argument("--window-size=800,600")

driver = webdriver.Chrome("./chromedriver", options=options)
driver.maximize_window()

#  Functions
def loop_accounts():
    accounts_data = open("accounts.txt", "r").readlines()
    accounts = {}
    for account in accounts_data:
        account_splited = account.split(":", maxsplit=1)
        #  Extract Email and Password from accounts.txt
        email = account_splited[0].strip()
        password = account_splited[1].strip()
        #  Login
        print("Start logging in for " + email)
        link = "https://engine.presearch.org/search?q=" + random.choice(words).strip()
        driver.get(link)
        sleep(3)
        driver.delete_all_cookies()
        driver.refresh()
        sleep(3)
        login_element = driver.find_element(By.XPATH, '//div[text()="Register or Login"]')
        login_element.click()
        
        driver.switch_to.window(driver.window_handles[1])

        email_input = driver.find_element(By.XPATH, '//input[@name="email"]')
        email_input.send_keys(email)
        
        password_input = driver.find_element(By.XPATH, '//input[@name="password"]')
        password_input.send_keys(password)
        
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()
      
        driver.switch_to.default_content()
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='recaptcha challenge expires in two minutes']")))

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.help-button-holder"))).click()
        sleep(12)
        
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.help-button-holder"))).click()
            sleep(12)
        except:
            pass
            
    
        driver.switch_to.default_content()
        password_input.submit()
        print("Logged in as " + email)
        sleep(5)
        driver.switch_to.window(driver.window_handles[0])
        sleep(5)
        loop_search()
        # winsound.Beep(2000, 1500)
        # input("Press enter to continue.")
        
        
        
def loop_search():
    link = "https://engine.presearch.org/search?q=" + random.choice(words).strip()
    driver.get(link)
    if config["random"]:
        for i in range(0, config["searches_count"]):
            word = random.choice(words).strip()
            search(word)
            print("Searched for " + word)
            sleep(max(config["delay"], 2))
    else:
        for word in words:
            word = word.strip()
            search(word)
            print("Searched for " + word)
            sleep(max(config["delay"], 2))


def search(word):
    search_bar = driver.find_element(By.NAME, "q")
    search_bar.clear()
    search_bar.send_keys(word)
    search_bar.submit()



if config["loop_accounts"]:
    loop_accounts()
else:
    loop_search()
  