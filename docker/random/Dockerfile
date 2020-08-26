FROM python:3.8-buster

# Timezone stuff
ENV TZ=Europe/Warsaw
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# force stdout and stderror to be unbuffered
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y vim python3-pip

WORKDIR /home

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY ./src /home/

CMD [ "python3", "app.py" ]

