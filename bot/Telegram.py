import time, requests, os
from bot import log
from constants import *

class Telegram:
    def __init__(self):
        self.api = f"{TELEGRAM_URL}bot{os.getenv('BOT_TOKEN')}"
        self.id = os.getenv('MY_ID')
 
    def send_message(self, dest, text, disable_notification):
        """
        Telegram text notification
        """
        url = f'{self.api}/sendMessage'
        data = dict(chat_id = dest, text = text, disable_notification = disable_notification)
        requests.post(url, data=data).json()

    def save_screenshot(self, elem, user):
        """
        Take a screenshot of an element
        """
        log(f"{COLORS['orange']}[+] Taking screenshot of {user}...{COLORS['clear']}")
        loc_time = time.localtime()
        time_string = time.strftime("%d-%m-%Y", loc_time)
        filename = f"{time_string}_{user}.png"
        elem.screenshot(filename)
        self.send_screenshot(self.id, filename)

    def send_screenshot(self, dest, filename):
        """
        Send a screenshot file
        """
        url = f'{self.api}/sendPhoto'
        file = {'photo': open(filename, "rb")}
        data = dict(chat_id = dest, disable_notification = True)
        requests.post(url, data = data, files = file).json()
        log('📤 Screenshot sent')
        os.remove(filename)