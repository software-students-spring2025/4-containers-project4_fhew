FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
