FROM python:3.9

RUN mkdir usr/app
WORKDIR usr/app

COPY . .

RUN pip install -r requirements.txt

RUN pip install bcrypt

CMD python app.py

