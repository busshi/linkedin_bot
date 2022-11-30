import os, time, pickle, logging
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import onetimepass as otp
from Telegram import *
from constants import *

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s %(message)s')

class Linkedin:
    def __init__(self, headless):
        """
        Init webdriver
        """

        options = FirefoxOptions()
        if headless:
            tg = Telegram()
            tg.send_message(tg.id, "✅ Starting bot...", True)    
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--disable-blink-features=AutomationControlled')
        self.username = os.getenv('USER_LOGIN')
        self.password = os.getenv('USER_PASS')
        self.token = os.getenv('TFA_SECRET')
        self.loop_timeout = LONG_TIMEOUT
        self.bot = webdriver.Firefox(options = options)
        #if not headless:
        self.bot.set_window_size(1980, 1200)

    def exit_failure(self, with_telegram):
        """
        Exit program
        """

        bot = self.bot
        logging.critical(f"{COLORS['red']}[+] Unable to login! Exiting...{COLORS['clear']}")
        if with_telegram:
            tg = Telegram()
            tg.send_message(tg.id, "❌ Bot exited!", True)
        bot.quit()
        exit (1)


    def is_logged_in(self, with_telegram):
        """
        Check if user still logged in
        """

        bot = self.bot
        try:
            if WebDriverWait(bot, timeout = 5).until(lambda d: d.find_element(By.TAG_NAME, 'a')).text == 'S’identifier':
                self.exit_failure(with_telegram)

            logging.info(f"{COLORS['green']}[+] Logged in{COLORS['clear']}")
            self.save_cookies()

        except TimeoutException:
            self.exit_failure(with_telegram)
    

    def save_cookies(self):
        """
        Store cookies in a file
        """

        with open(COOKIES_FILE, 'wb') as f:
            pickle.dump(self.bot.get_cookies(), f)


    def load_cookies(self):
        """
        Load cookies from a file
        """

        with open(COOKIES_FILE, 'rb') as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                self.bot.add_cookie(cookie)


    def login(self):
        """
        Login to Linkedin
        """

        bot = self.bot
#        bot.fullscreen_window()
        bot.get(LINKEDIN_URL)

        try:
            email = WebDriverWait(bot, timeout = 3).until(lambda d: d.find_element(By.ID, DOM_VARIABLES['login_user']))
            email.send_keys(self.username)
            password = WebDriverWait(bot, timeout = 3).until(lambda d: d.find_element(By.ID, DOM_VARIABLES['login_password']))
            password.send_keys(self.password)
            password.send_keys(Keys.RETURN)
            logging.info(f"{COLORS['orange']}[+] Loging in...{COLORS['clear']}")
        
        except Exception:
            logging.critical(f"{COLORS['red']}[+] Unable to login! Exiting...{COLORS['clear']}")
            exit (1)
        

        ### HUMAN CHECK
        try:
            WebDriverWait(bot, timeout = 5).until(lambda d: d.find_element(By.XPATH, DOM_VARIABLES['human_check']))
            logging.error(f"{COLORS['red']}[+] Human validation needed! Check the browser.{COLORS['clear']}")
            for i in range(11):
                if i == 10:
                    print('\r0') 
                else:
                    print(f'\r{10 - i} ', end='')
                time.sleep(1)

        except TimeoutException:
            logging.info(f"{COLORS['green']}[+] Apparently logged in{COLORS['clear']}")


        ### TFA
        try:
            tfa = WebDriverWait(bot, timeout = 5).until(lambda d: d.find_element(By.ID, DOM_VARIABLES['tfa_pin']))
            logging.warning('[+] TFA required to login')
            tfa_code = otp.get_totp(self.token)
            tfa.send_keys(tfa_code)
            tfa.send_keys(Keys.RETURN)
            time.sleep(3)

        except TimeoutException:
            pass
            

    def check_network(self, with_telegram):
        """
        Check incoming connexion requests
        """

        logging.info(f"{COLORS['orange']}[+] Checking new connexions requests...{COLORS['clear']}")
        bot = self.bot
        bot.get(LINKEDIN_NETWORK_URL)
        
        try:
  #          WebDriverWait(bot, timeout = 10).until(EC.presence_of_all_elements_located((By.XPATH, DOM_VARIABLES['reduce_messaging'])))
    #    WebDriverWait(bot, timeout = 10).until(EC.element_to_be_clickable((By.CLASS_NAME, DOM_VARIABLES['reduce_messaging'])))
#        buttons = WebDriverWait(bot, timeout = 10).until(lambda d: d.find_elements(By.XPATH, DOM_VARIABLES['reduce_messaging'])) #.click() #.click()
                #ActionChains(bot).move_to_element(buttons).click().perform()
#            if (len(buttons) > 1):
 #               time.sleep(3)
  #  buttons[len(buttons) - 1].click()
            WebDriverWait(bot, timeout = 10).until(lambda d: d.find_element(By.XPATH, DOM_VARIABLES['reduce_messaging'])).click()
            time.sleep(2)
            bot.get(LINKEDIN_NETWORK_URL)
 
        except:
            logging.info('👥 Network skipped')
            return

        while True:
            try:
                WebDriverWait(bot, timeout = 10).until(lambda d: d.find_elements(By.CLASS_NAME, DOM_VARIABLES['new_connexion']))
            except TimeoutException:
                logging.info('👥 Network checked')
                break
            finally :
                invits = bot.find_elements(By.CLASS_NAME, DOM_VARIABLES['connexion_request'])
                for elem in invits:
                    invit = elem.get_attribute("aria-label")
                    username = str(invit)[25:]
                    if 'Accepter' in elem.text:
                        logging.info(f"✋ New connexion request from {username}")
                        if with_telegram:
                            tg = Telegram()
                            icon = WebDriverWait(bot, timeout = 5).until(lambda d: d.find_element(By.CSS_SELECTOR, f"[alt^='Photo de {username}']"))
                            tg.send_message(tg.id, f"✋ New connexion request from {username}", False)
                            self.save_screenshot(icon, username, tg)

                        ActionChains(bot).move_to_element(bot.find_element(By.XPATH, DOM_VARIABLES['accept_connexion'])).click().perform()
#                        WebDriverWait(bot, timeout = 8).until(EC.presence_of_element_located((By.XPATH, DOM_VARIABLES['accept_connexion']))).click()
                        #WebDriverWait(bot, timeout = 5).until(lambda d: d.find_element(By.XPATH, DOM_VARIABLES['accept_connexion'])).click()
                        WebDriverWait(bot, timeout = 5).until(lambda d: d.find_element(By.XPATH, DOM_VARIABLES['write_message'])).click()                        
                        self.send_welcome_message(username, with_telegram)
                        self.loop_timeout = SHORT_TIMEOUT

                break


    def check_messages(self, with_telegram):
        """
        Check messaging to auto send welcome message and handle bot actions
        """

        bot = self.bot
        bot.get(LINKEDIN_MESSAGES_URL)
        logging.info(f"{COLORS['orange']}[+] Checking new unread messages...{COLORS['clear']}")
        try:
            messages = WebDriverWait(bot, timeout=8).until(lambda d: d.find_elements(By.CLASS_NAME, DOM_VARIABLES['unread_message']))
            if not len(messages):
                logging.info('No new message')

            for message in messages:
                logging.info('📥 New message:')
                print (message.text)
                if with_telegram:
                    tg = Telegram()
                    tg.send_message(tg.id, f"📥 New unread message from {message.text}", True)
                message.click()

                index = message.text.find(':')
                action = message.text[index + 2:].lower()
                if action[:2] == '- ':
                    action = action[2:] 
                elif action[0] == '-':
                    action = action[1:] 

                try:
                    username = WebDriverWait(bot, timeout = 10).until(lambda d: d.find_element(By.ID, DOM_VARIABLES['username'])).text
                except:
                    username = message.text[:index - 1]

                contacts_file = open(CONTACTS_FILE, 'r')
                contacts = contacts_file.read()
                contacts_file.close()
                is_bot_muted = True if f'{username}_muted\n' in contacts else False
                is_new_contact = False if username in contacts else True

                if not is_bot_muted and is_new_contact:
                    self.send_welcome_message(username, with_telegram)
                    self.loop_timeout = SHORT_TIMEOUT
                    

                elif (not is_bot_muted and not is_new_contact and action in ACTIONS) or (is_bot_muted and action == 'unmute'):
                    self.actions_reply(action, username, with_telegram)
                    self.loop_timeout = SHORT_TIMEOUT


        except TimeoutException:
            logging.info('📨 Messages checked...')
    

    def send_welcome_message(self, username, with_telegram):
        """
        Send welcome message and add contact to list
        """

        logging.info(f"{COLORS['orange']}[+] Sending welcome message to {username}{COLORS['clear']}")
        bot = self.bot
        input_form = WebDriverWait(bot, timeout = 5).until(lambda d: d.find_element(By.CSS_SELECTOR, DOM_VARIABLES['message_input_form']))
        for msg in WELCOME_MESSAGE:
            input_form.send_keys(msg)
            input_form.send_keys(Keys.RETURN)
            time.sleep(1)

        if with_telegram:
            tg = Telegram()
            tg.send_message(tg.id, f"📤 Welcome message sent to [{username}]", True)
        
        with open(CONTACTS_FILE, 'a') as f:
            f.write(f'{username}\n')
            f.close()
                        

    def actions_reply(self, action, username, with_telegram):
        """
        Handle bot actions :
            - profile
            - techno
            - dispo
            - contact
            - unmute
        """

        logging.info(f"[+] Action [{action}] required by [{username}]")
        bot = self.bot
        input_form = WebDriverWait(bot, timeout = 5).until(lambda d: d.find_element(By.CSS_SELECTOR, DOM_VARIABLES['message_input_form']))
        for msg in ACTIONS[action]:
            input_form.send_keys(msg)
            input_form.send_keys(Keys.RETURN)
            time.sleep(1)

        if with_telegram:
            tg = Telegram()
            tg.send_message(tg.id, f"🗣️ Action [{action}] asked by [{username}]", True)
        
        if action == 'contact' or action == 'unmute':
            contacts_file = open(CONTACTS_FILE, 'r')
            contacts = contacts_file.read()
            contacts_file.close()
            contacts_file = open(CONTACTS_FILE, 'w')

            if action == 'contact':
                contacts_file.write(contacts.replace(username, f'{username}_muted'))
                if with_telegram:
                    tg.send_message(tg.id, f"🚨 [{username}] wants to talk with you...", False)
            
            elif action == 'unmute':
                contacts_file.write(contacts.replace(f'{username}_muted', username))

            contacts_file.close()


    def save_screenshot(self, elem, user, tg):
        """
        Take a screenshot of an element
        """
        logging.info(f"{COLORS['orange']}[+] Taking screenshot of {user}...{COLORS['clear']}")
        loc_time = time.localtime()
        time_string = time.strftime("%d-%m-%Y", loc_time)
        filename = f"{time_string}_{user}.png"
        elem.screenshot(filename)      
        tg.send_photo(tg.id, filename)
        logging.info('📤 Screenshot sent')

