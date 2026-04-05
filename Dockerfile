FROM python:3.12-slim

WORKDIR /app

COPY . /app/

WORKDIR /app/capsula_tempo

RUN pip install --upgrade pip
RUN pip install -r ../requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]