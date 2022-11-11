#!/usr/bin/env python3
# coding=utf-8

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
#from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
#import onetimepass as otp
import time, requests, os, sys
from dotenv import load_dotenv

load_dotenv()

RED = '\033[31m'
GREEN = '\033[32m'
ORANGE = '\033[34m'
CLR = '\033[0m'

class Telegram:
    def __init__(self):
        self.api = f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}"
        self.id = os.getenv('MY_ID')
 
    def send_message(self, dest, txt):
        url = f'{self.api}/sendMessage'
        data = dict(chat_id=dest, text=txt, disable_notification=True)
        requests.post(url, data=data).json()

    def save_screenshot(self, elem):
        print(f'{ORANGE}[+] Taking screenshot of the new connexion request...{CLR}')
        loc_time = time.localtime()
        time_string = time.strftime("%d-%m-%Y", loc_time)
        filename = time_string + "_screenshot.png"
        elem.screenshot(filename)
        self.send_screenshot(self.id, filename)

    def send_screenshot(self, dest, file):
        url = f'{self.api}/sendPhoto'
        file = {'photo': open(file, "rb")}
        data = dict(chat_id=dest, disable_notification=True)
        requests.post(url, data=data, files=file).json()

class Linkedin:
    def __init__(self):
        options = FirefoxOptions()
#        options.add_argument("--headless")
        options.add_argument('--disable-blink-features=AutomationControlled')
        self.username = os.getenv('USER_LOGIN')
        self.password = os.getenv('USER_PASS')
        self.token = os.getenv('TFA_SECRET')
        self.bot = webdriver.Firefox(options=options)

    def login(self):
        bot = self.bot
        bot.get("https://linkedin.com/")
#        time.sleep(3)

        try:
            email = WebDriverWait(bot, timeout=3).until(lambda d: d.find_element(By.ID, "session_key"))
#            email = bot.find_element("id", "session_key")
            email.send_keys(self.username)
            password = WebDriverWait(bot, timeout=3).until(lambda d: d.find_element(By.ID, "session_password"))
#            password = bot.find_element("id", "session_password")
            password.send_keys(self.password)
            password.send_keys(Keys.RETURN)
            print(f'{ORANGE}[+] Loging in...{CLR}')
        
            ### HUMAN CHECK
            try:
                time.sleep(5)
                bot.find_element(By.XPATH, "//*[text()='Procédons à une petite vérification de sécurité']")
                print(f'${RED}[+] Manual validation required! Check the browser.\033{CLR}')
                time.sleep(10)

            except:
                print(f'{GREEN}[+] Logged in{CLR}')

            ### TFA
            #time.sleep(5)
            # tfa_code = otp.get_totp(self.token)
            # tfa = bot.find_element("id", "input__phone_verification_pin")
            # tfa.send_keys(tfa_code)
            # tfa.send_keys(Keys.RETURN)

        except Exception:
            print (f'{RED}Unable to login! Exiting...{CLR}')
            exit (1)

    # def skip_phone(self):
    #     time.sleep(3)
    #     bot = self.bot
    #     try:
    #         bot.find_element("id", "my-id").Click()
    #     except Exception as e:
    #         print (e)

    def check_network(self, with_telegram):
#        time.sleep(5)
        bot = self.bot
        try:
            network = WebDriverWait(bot, timeout=5).until(lambda d: d.find_element(By.CLASS_NAME, "msg-overlay-bubble-header__controls display-flex"))
            network.click()
        except:
            print('ok')

        print(f'{ORANGE}[+] Checking new connexions requests...{CLR}')
#        try:
        bot.get("https://www.linkedin.com/mynetwork/")
#            bot.find_element(By.CSS_SELECTOR, "[title^='Réseau']").click()
#        time.sleep(3)
#            nothing = ''
 #           try:
  #              nothing = bot.find_element(By.XPATH, "//*[text()='Aucune invitation en attente']")
   #         except:
    #            nothing = ''

     #       if nothing == '':
#        element_exists = True
        while True:
            try:
                WebDriverWait(bot, timeout=5).until(lambda d: d.find_elements(By.CLASS_NAME, "invitation-card__action-btn"))
#                bot.find_elements(By.CLASS_NAME, "invitation-card__action-btn")
            except NoSuchElementException:
                #element_exists = False
                break
            finally :
#                if element_exists:
#                        bot.find_element_by_class_name("invitation-card__action-btn artdeco-button--secondary").click()
                invits = bot.find_elements(By.CLASS_NAME, "artdeco-button--secondary")
#                    invits = bot.find_elements(By.CLASS_NAME, "invitation-card artdeco-list__item")
#                print(len(invits))
                for elem in invits:
                    invit = elem.get_attribute("aria-label")
                    user = str(invit)[25:]
                    if 'Accepter' in elem.text:
                        if with_telegram:
                            print(f"New connexion request from {user}")
                            tg = Telegram()
                            icon = bot.find_element(By.CSS_SELECTOR, f"[alt^='Photo de {user}']")
                            tg.send_message(tg.id, f"New connexion request from {user}")
                            tg.save_screenshot(icon)
#                        elem.click()
#                    element_exists = False
                break

    def check_messages(self):
        time.sleep(3)
        print(f'{ORANGE}[+] Checking new unread messages...{CLR}')
        bot = self.bot
        try:
            messages = bot.find_elements(By.CLASS_NAME, "notification-badge__count ")
            if len(messages):
                print('[+] New message(s)', messages)
            else:
                print('[+] No new message...')
        except Exception as e:
            print (e)
            bot.quit()

def run(with_telegram):
    try:
        linkedin = Linkedin()
        linkedin.login()
        #linkedin.skip_phone()
        while True:
            linkedin.check_network(with_telegram)
            linkedin.check_messages()
            time.sleep(30)

    except KeyboardInterrupt:
        print('Exit.')
        linkedin.bot.quit()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        run(False)
    elif len(sys.argv) == 2 and sys.argv[1] == '-tg':
        run(True)
    else:
        print('Usage: ./bot.py [-tg OPTIONAL]')