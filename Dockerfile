FROM        ubuntu:20.04

ENV         DEBIAN_FRONTEND=noninteractive 

WORKDIR     /opt/app/bot

COPY        bot/ .

RUN         apt-get update && apt-get install -y \
            python3 python3-pip firefox-geckodriver xvfb \
            && rm -rf /var/lib/apt/lists/*

RUN			useradd -m -s /bin/bash linkedin

RUN			chown -R linkedin:linkedin /opt/app/bot

USER        linkedin

RUN         firefox -CreateProfile "headless /moz-headless" -headless

RUN         pip3 install --no-cache-dir selenium onetimepass requests \
            python-dotenv

ENTRYPOINT [ "python3", "bot.py", "--telegram", "--headless" ]