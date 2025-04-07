FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Install pipenv
RUN pip install --upgrade pip && pip install pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile

COPY . .

RUN mkdir -p /app/static

CMD ["python", "ml_client.py"]
