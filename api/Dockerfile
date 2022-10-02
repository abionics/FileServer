FROM python:3.10-slim
RUN apt-get update
RUN apt-get install -y libmagic1
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers", "--forwarded-allow-ips", "*"]
