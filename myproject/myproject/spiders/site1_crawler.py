import scrapy
from bs4 import BeautifulSoup

class Site1_Crawler(scrapy.Spider):
    name = "site1_crawler"
    allowed_domains = ["thethao247.vn"]
    start_urls = ["https://thethao247.vn/livescores/chau-au/champions-league/results/"]

    def parse(self, response):

        soup = BeautifulSoup(response.text, "html.parser")
        # where to extract data
        container = soup.find('div', class_='data')

        # extract first team
        home_teams = container.find_all('div', class_='team team-a')

        # extract score
        scores = container.find_all('div', class_='score')

        # extract second team
        away_teams = container.find_all('div', class_='team team-b')

        # extract urls
        urlsDiv = container.find('div', class_='more')
        urls = [link['href'] for link in urlsDiv.find_all('a', class_='name')]
        
        # yield formatted data to container and csv file
        for home_team, score, away_team, url in zip(home_teams, scores, away_teams, urls):
            yield response.follow(url, self.parse_job, meta={
                'doi_nha': home_team.text.strip(),
                'ti_so': " ".join(score.text.strip().split()),
                'doi_khach': away_team.text.strip(),
            })

    def parse_job(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        # extract match dates and times
        dates = soup.find('div', class_='text-muted fs-12')

        # extract match status
        status = soup.find('div', class_='status fw-bold text-danger start-time-event')

        yield {
            'ngay_thi_dau': dates.text.strip() if dates else None,
            'trang_thai': status.text.strip() if status else None,
            'doi_nha': response.meta['doi_nha'],
            'ti_so': response.meta['ti_so'],
            'doi_khach': response.meta['doi_khach'],
            'url': response.url
        }
