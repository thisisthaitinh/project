import scrapy
from bs4 import BeautifulSoup


class Site3Crawler(scrapy.Spider):
    name = "site3_crawler"
    allowed_domains = ["propzy.net"]
    start_urls = ["https://propzy.net/bat-dong-san/", "https://propzy.net/bat-dong-san/page/2/", "https://propzy.net/bat-dong-san/page/3/"]

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        # where to extract data
        container = soup.find('div', class_='content_right')

        # title
        titles = soup.find_all('h3')

        # article links
        links = container.find_all('a')

        # yield formatted data to table and csv file
        for title, link in zip(titles, links):
            article_link = link['href']
            yield response.follow(article_link, self.parse_article, meta={
                'title': title.text.strip(),
            })

    def parse_article(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        # extract locations
        locationsInfo = soup.find('div', class_='prop-diachi')
        locations = locationsInfo.find('span', class_='content')

        # extract areas
        areasInfo = soup.find('div', class_='prop-dientich')
        areas = areasInfo.find('span', class_='content')

        # extract prices
        pricesInfo = soup.find('div', class_='prop-price')
        prices = pricesInfo.find('span', class_='content')

        # extract information details
        infoDetails = soup.find('div', class_='prop-features prop-after')
        info = infoDetails.find_all('span')
        infoList = [i.text.strip() for i in info]
        infoString = ', '.join(infoList)

        yield {
            'title': response.meta['title'],
            'location': locations.text.strip() if locations else None,
            'area': areas.text.strip() if areas else None,
            'price': prices.text.strip() if prices else None,
            'details': infoString if infoString else None,
            'url': response.url
        }