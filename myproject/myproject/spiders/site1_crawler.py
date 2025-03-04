import scrapy
from bs4 import BeautifulSoup

class Site1_Crawler(scrapy.Spider):
    name = "site1_crawler"
    allowed_domains = ["thethao247.vn"]
    start_urls = ["https://thethao247.vn/livescores/chau-au/champions-league/results/"]

    def parse(self, response):

        soup = BeautifulSoup(response.text, "html.parser")
        # where to extract data
        table = soup.find('div', class_='data')

        # extract match time
        times =  table.find_all('span', class_='time')

        # extract first team
        home_teams = table.find_all('div', class_='team team-a')

        # extract score
        scores = table.find_all('div', class_='score')

        # extract second team
        away_teams = table.find_all('div', class_='team team-b')
        
        # yield formatted data to table and csv file
        for time, home_team, score, away_team in zip(times, home_teams, scores, away_teams):
            yield {
                'thoi_gian': time.text.strip(),
                'doi_nha': home_team.text.strip(),
                'ti_so': " ".join(score.text.strip().split()),
                'doi_khach': away_team.text.strip(),
            }

        
