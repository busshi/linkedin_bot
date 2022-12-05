![deploy](https://github.com/busshi/linkedin_bot/actions/workflows/build.yml/badge.svg)

# Linkedin Bot / Selenium

### A basic linkedin bot used to accept incoming connexions requests coded in Python.

## Functionalities:

- Autologin with TFA enabled (optional)
- Accept connexions requests
- Send an automatic welcome message inside my network
- Autoreply to messages from new contacts and send actions keywords:
  - dispo
  - techno
  - profile
  - contact
  - unmute
- Send notifications to a Telegram account (userID needed, get yours with [Telegram API](https://core.telegram.org/bots/api#getting-updates)) using a telegram bot (you can easily create one with [BotFather](https://telegram.me/BotFather)) with new connexions requests and profile picture

## Usage

- Install dependencies `pip install -r requirements.txt`
- Copy env.sample to a .env file a replace with your custom values
- Run the bot without options `python3 bot/bot.py`
- Run the bot with Telegram support `python3 bot/bot.py --telegram`
- Run the bot without visualization `python3 bot/bot.py --headless`
- Combine both options `python3 bot/bot.py --telegram --headless`

## Docker usage

Before use docker, think about login in a virtual environment to get a cookie. It will avoid human captch verification. Then you will be able to run it headless inside a container.

`docker-compose up -d`

## Notes

- This bot uses [Selenium](https://selenium.dev) and the Firefox webdriver so you will probably need Firefox to be installed on your system.
- Sometimes, after login in, you can have a captcha to validate manually. You will have a message in the console and 10 seconds to validate the captcha.
- As Selenium uses classnames, ids, xpath to find elements, it is possible it will not work anymore in the future without updating DOM_VARIABLES (inside constants.py file). This bot was created to work with a french browser, so classnames are in french...
- Tested on macOS.
- Also available on [Dockerhub](https://hub.docker.com/r/busshi/linkedin_bot)

## Todos

- [x] Use Linkedin API to avoid captcha -> [here](https://github.com/busshi/linkedin_bot_api)
- [x] Dockerize service
- [ ] Intl
