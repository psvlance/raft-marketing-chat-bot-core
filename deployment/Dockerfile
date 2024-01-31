FROM python:3.10

WORKDIR /app

RUN python -m pip install --upgrade pip pip-tools

ENV PATH=$PATH:/app/vendor/bin
ENV PYTHONPATH=$PYTHONPATH:/app/vendor/lib/python3.10/site-packages
ENV PYTHONUNBUFFERED=1
ENV API_TOKEN=6458815613:AAFDxVL_J6_kkuOhxDn57cmejB9x8XaQzlw

COPY raft-marketing-chat-bot/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# TODO prod stuff
#COPY raft-marketing-chat-bot/src/ /app
