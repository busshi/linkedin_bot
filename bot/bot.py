#!/usr/bin/env python3
# coding=utf-8

import time, sys
from dotenv import load_dotenv
#from pyvirtualdisplay import Display
from Linkedin import *
import argparse

load_dotenv()

def run(args):
    try:
        with_telegram = args.telegram
        headless = args.headless
        # display = Display(visible=0, size=(1980, 1200))
        # display.start()
        linkedin = Linkedin(headless)
        if os.path.exists(COOKIES_FILE):
            linkedin.bot.get(LINKEDIN_URL)
            linkedin.load_cookies()
            linkedin.bot.get(LINKEDIN_URL)
        else:
            linkedin.login()

        x = 0
        while True:
            linkedin.is_logged_in(with_telegram)
            if x == 10:
                x = 0
                linkedin.loop_timeout = LONG_TIMEOUT
            if x == 0:
                linkedin.check_network(with_telegram)
            linkedin.check_messages(with_telegram)
            time.sleep(linkedin.loop_timeout)
            x += 1

    except KeyboardInterrupt:
        linkedin.bot.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--headless", action='store_true', help="without vizualisation")
    parser.add_argument("--telegram", "-t", action='store_true', help="with Telegram notifications")
    args = parser.parse_args()

    run(args)
