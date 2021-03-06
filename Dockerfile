FROM python:3

ENV DISCORD_TOKEN=""
ENV DISCORD_GUILD=""
ENV TIMEZONE="Europe/Berlin"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./bot.py" ]