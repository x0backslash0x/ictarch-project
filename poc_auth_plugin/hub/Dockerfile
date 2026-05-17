FROM python:3.11-slim

WORKDIR /hub

COPY . /hub

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]