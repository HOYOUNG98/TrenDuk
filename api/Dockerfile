FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN pip3 install gunicorn

ENV FLASK_APP app
ENV FLASK_ENV production

EXPOSE 5000

CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "wsgi:app"]
