from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from twilio.http.http_client import TwilioHttpClient
import time
import os
from dotenv import load_dotenv
load_dotenv()

from_number = os.environ["from_number"]
to_number = os.environ["to_number"]
account_sid = os.environ["account_sid"]
auth_token = os.environ["auth_token"]
url = "https://tickets.funcode.hu/event/suicideboys-2023/pyos"



options = webdriver.ChromeOptions()
# options.add_argument("--no-sandbox")
# options.add_argument('--headless')
# options.add_argument('--disable-gpu') 
# options.headless = True
options.add_argument('--headless=new')#ASTA E BUN yayy
options.add_argument("--user-data-dir=/Users/viktorashi/Library/Application Support/Google/Chrome/")
options.add_argument('--profile-directory=Profile 1')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)


def isAvailable():
    driver.get(url)
    try :
    
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/article/div[1]/section[2]/form/div[1]/div[2]/input[1]'))).click()
    except:
        print("No button")    
    #wait for element to be clickable
    iframe = WebDriverWait(driver, 10).until(
EC.presence_of_element_located(('xpath', '/html/body/article/article/div/section[1]/div[2]/div/iframe')))
    
    #click it around the middle to the left i guess
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(iframe, -50, 0)
    action.click()
    time.sleep(3)
    action.perform()
    driver.switch_to.frame(iframe)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div[3]/div[2]/div[2]/div/div[2]/div/button[2]'))).click()
    # time.sleep(4)
    # driver.find_element('xpath', '/html/body/div[3]/div[2]/div[3]/div[2]/div[2]/div/div[2]/div/button[2]').click()
    driver.switch_to.default_content()
    time.sleep(4)
    notify =''
    try:
        notify = WebDriverWait(driver, 5).until(EC.presence_of_element_located(('xpath', '/html/body/article/article/div/section[1]/div[4]/div/span')))
        notify2 = WebDriverWait(driver, 5).until(EC.presence_of_element_located(('xpath', '//*[@id="notify_message"]/span')))
        if notify or notify2:
            try:
                print(1)
                print(notify.text)
                print(2)
                print(notify2.text)
            except:
                print("Am gasit mesajele alea da sunt elemente cum crezi tu")
                return True
    except:
        print("No notify")
        return True
    
    #these are error messages that appear when the tickets are not available
    possible_messages = ["This category is currently unavailable", "This category is currently unavailable", "Please select another category.", "Unable to reserve 1 tickets", 'Unable to reserve 1 tickets for $uicideboy$ present Gray Day Europe Tour 2023 Standing - PL2', 'Jelenleg ez a kategória nem elérhető']

    #check if any of the messages from the list are in the notify.text
    if any(x in notify.text for x in possible_messages):
        return False
    else:
    #check if there are ANY elements that contain the messages from the list
        for message in possible_messages:
            try:
                el = driver.find_element('xpath',"//*[contains(text(), {}')]".format(message))
                print("For the {}" .format(message))
                print(el.text)
                return False
            #if it finds something that is not an error message
            except:
                print("printing the original notify")
                print(notify.text)
            
    return notify


def send_text_message(message):
    client = Client(account_sid, auth_token)
    try:
        client.messages.create(
            to=to_number,
            from_=from_number,
            body=message
        )
        print("Message sent")
    except TwilioRestException as e:
        print(e)
            
       
def KeepTryn():
    while True:
        available = isAvailable()
        if available:
            print("Available!!!!!!")
            send_text_message("!!!!!!!!!!!BAA HAI REPEDE LA LAPTOP CA-AM GASIT CEVA!!!!!!!!!!!!!!!!!")
            print(available)
            try:
                print(available.text)
            except:
                send_text_message("L-AM GASIT da n-are text in el nuj hai sa vezi")
                print("L-AM GASIT da n-are text in el nuj hai sa vezi")
            print("bruh")
        else:
            print("Not available")
        time.sleep(20)


KeepTryn()
