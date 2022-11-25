#!/usr/bin/env python3
# coding=utf-8

import time, sys
from dotenv import load_dotenv
from Linkedin import *

load_dotenv()

def run(args):
    try:
        with_telegram = True if '--telegram' in args else False
        headless = True if '--headless' in args else False
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
    args = []
    if len(sys.argv) == 1:
        run([])
    elif len(sys.argv) >= 2:
        for arg in sys.argv:
            if arg in ARGS_LIST:
                args.append(arg)
            elif arg == sys.argv[0]:
                pass
            else:
                print('Usage: ./bot.py [--telegram --headless]')
                exit (1)
        run(args)
    else:
        print('Usage: ./bot.py [--telegram --headless]')
