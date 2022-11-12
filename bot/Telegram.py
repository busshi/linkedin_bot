import requests, os
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

    def send_photo(self, dest, filename):
        """
        Send a photo file
        """
        url = f'{self.api}/sendPhoto'
        file = {'photo': open(filename, "rb")}
        data = dict(chat_id = dest, disable_notification = True)
        requests.post(url, data = data, files = file).json()
        os.remove(filename)