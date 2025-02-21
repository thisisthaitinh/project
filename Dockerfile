FROM python:3.9-slim

WORKDIR /app/myproject

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["scrapy", "crawl", "site1_crawler", "-o", "output1.csv"]