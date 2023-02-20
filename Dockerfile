FROM python:3.9

WORKDIR /Home/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]
