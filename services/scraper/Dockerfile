FROM python:3.12.7-alpine3.20

WORKDIR /app

COPY requirements-lock.txt .

RUN pip install --upgrade pip \
&& pip install --no-cache-dir -r requirements-lock.txt

COPY . .

CMD ["python", "main.py"]
