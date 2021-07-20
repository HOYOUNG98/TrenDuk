FROM python:3.8-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP app
ENV FLASK_ENV production

EXPOSE 5000

CMD [ "python3", "app.py"]