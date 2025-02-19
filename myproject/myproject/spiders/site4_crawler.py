import scrapy
from bs4 import BeautifulSoup

class Site4Crawler(scrapy.Spider):
    name = "site4_crawler"
    allowed_domains = ["careerviet.vn"]
    start_urls = ["https://careerviet.vn/viec-lam/tat-ca-viec-lam-vi.html"]

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        # where to extract data
        container = soup.find('div', class_='main-slide')

        # job titles
        job = container.find_all('div', class_='title')
        job_titles = [j.text.strip().replace("(Mới)", "").strip() for j in job]

        # company names
        companies = container.find_all('a', class_='company-name')
        company_names = [c.text.strip() for c in companies]

        # salaries
        salaries = container.find_all('div', class_='salary')
        salariesAmount = [s.text.strip().replace("Lương: ", "").strip() for s in salaries]

        # locations
        locations = [l.text.strip() for l in container.find_all('div', class_='location')]

        # links
        links = [link['href'] for link in container.find_all('a', class_='job_link')]

        # yield
        for job_title, company_name, location, salary, link in zip(job_titles, company_names, locations, salariesAmount, links):
            yield response.follow(link, self.parse_job, meta={
                'job_title': job_title,
                'company_name': company_name,
                'salary': salary,
                'location': location
            })
    
    def parse_job(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        # yield
        yield {
            'job_title': response.meta['job_title'],
            'company_name': response.meta['company_name'],
            'salary': response.meta['salary'],
            'location': response.meta['location'],
            'url': response.url
        }

