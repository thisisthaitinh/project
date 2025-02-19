import scrapy
from bs4 import BeautifulSoup


class Site2Crawler(scrapy.Spider):
    name = "site2_crawler"
    allowed_domains = ["dantri.com.vn"]
    start_urls = ["https://dantri.com.vn/"]

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        # where to extract data
        container = soup.find('article', class_='article-list')

        # title
        titles = container.find_all('h3', class_='article-title')

        # description
        descriptions = container.find_all('div', class_='article-excerpt')

        # link
        links = container.find_all('a')

        # yield formatted data to table and csv file
        for title, description, link in zip(titles, descriptions, links):
            article_link = link['href']
            yield response.follow(article_link, self.parse_article, meta={
                'title': title.text.strip(),
                'description': description.text.strip(),
            })

    def parse_article(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        # extract categories
        # categories = soup.find('div', class_='cate-24h-foot-arti-deta-cre')

        # extract posted times
        posted_times = soup.find('time', class_='author-time')

        # extract authors
        authors = soup.find('div', class_='author-name')

        yield {
            'title': response.meta['title'],
            'description': response.meta['description'],
            'link': response.url,
            'posted_time': posted_times.text.strip() if posted_times else None,
            'author': authors.text.strip() if authors else None,
        }
