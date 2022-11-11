# Linkedin Bot / Selenium

### A basic linkedin bot used to accept incoming connexions requests code in Python.

## Functionalities:

- Autologin with TFA enabled (optional)
- Accept connexions requests
- Send an automatic welcome message inside my network
- Autoreply to messages from new contacts and send actions keywords:
  - dispo
  - techno
  - profile
- Optional: send messages to a Telegram user with a telegram bot (created with BotFather) with new connexions requests and profile picture

## Usage

- Install dependencies `pip install -r requirements.txt`
- Copy env.sample to a .env file a replace with your custom values
- Run the bot `python3 bot.py`
- Run the bot with Telegram support `python3 bot.py -tg`

## Notes

- This bot uses [Selenium](https://selenium.dev) and the Firefox webdriver so you will probably need Firefox to be installed on your system.
- Sometimes, after login in, you can have a captcha to validate manually. You will have a message in the console and 10 seconds to validate the captcha.
- Tested on macOS.

## TODOS

- Use Linkedin API to avoid captcha
- Dockerize service
