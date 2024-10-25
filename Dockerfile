FROM python:3.11-slim

COPY ./src /src

WORKDIR /src

RUN pip install -U pip && pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]