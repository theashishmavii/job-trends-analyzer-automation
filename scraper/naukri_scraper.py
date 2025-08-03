# scraper/naukri_scraper.py
from bs4 import BeautifulSoup
from .base_scraper import BaseScrapper

class NaukriScraper(BaseScrapper):
    BASE_URL = "https://www.naukri.com/"

    def build_url(self, filters):
        keywords=(filters.get("keywords","developer") or "developer").replace(' ', '-')
        location=(filters.get("location", "india") or "india").replace(' ', '-')
        params=[]

        if filters.get("date_posted") and filters["date_posted"] != "any":
            params.append(f"last-{filters['date_posted']}-days")

        if filters.get("remote"):
            params.append("work-from-home-remote")

        param_str = "-".join(params)
        if param_str:
            url = f"{self.BASE_URL}{keywords}-jobs-in-{location}-{param_str}"
        else:
            url = f"{self.BASE_URL}{keywords}-jobs-in-{location}"
        
        return url
    
    def parse_jobs(self, html):
        soup = BeautifulSoup(html,"html.parser")
        jobs=[]
        for card in soup.select('article.jobTuple'):
            title_el = card.select_one(".title")
            company_el = card.select_one(".companyName")
            loc_el = card.select_one(".location")
            exp_el = card.select_one(".experience")
            sal_el = card.select_one(".salary")
            job = {
                "title": title_el.text.strip() if title_el else "",
                "company": company_el.text.strip() if company_el else "",
                "location": loc_el.text.strip() if loc_el else "",
                "experience": exp_el.text.strip() if exp_el else "",
                "salary": sal_el.text.strip() if sal_el else "",
                "url": title_el['href'] if (title_el and title_el.has_attr('href')) else ""
            }
            jobs.append(job)
        return jobs