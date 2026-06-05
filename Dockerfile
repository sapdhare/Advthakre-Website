FROM python:3.13

WORKDIR /app

RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]