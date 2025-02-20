FROM python:3.9-slim

WORKDIR /app/myproject

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["scrapy", "crawl", "site1_crawler", "-o", "output1.csv"]