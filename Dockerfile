FROM        ubuntu:20.04

ENV         DEBIAN_FRONTEND=noninteractive 

COPY        bot/ /opt/app/bot

WORKDIR     /opt/app/bot

RUN         apt-get update && apt-get install -y \
            python3 python3-pip firefox-geckodriver xvfb \
            && rm -rf /var/lib/apt/lists/*

RUN         pip3 install --no-cache-dir selenium onetimepass requests python-dotenv

RUN         firefox -CreateProfile "headless /moz-headless" -headless

ENTRYPOINT [ "python3", "bot.py", "--telegram", "--headless" ]