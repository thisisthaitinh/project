FROM python:3.9-slim

WORKDIR /app/myproject

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["scrapy", "crawl", "site2_crawler", "-o", "output2.csv"]