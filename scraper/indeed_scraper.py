# scraper/indeed_scraper.py
from bs4 import BeautifulSoup
from .base_scraper import BaseScrapper
from urllib.parse import urlencode

class IndeedScraper(BaseScrapper):
    BASE_URL = "https://in.indeed.com/jobs?"

    def build_url(self, filters):
        params = {
            "q":filters.get("keywords",""),
            "l":filters.get("location",""),
        }
        # Date posted (fromage): 1=24h, 3=3d, 7=7d, 14=14d
        if filters.get("date_posted") and filters["date_posted"] != "any":
            params["fromage"] = str(filters["date_posted"])

        types = filters.get("job_type",[])
        if types:
            params["jt"] = types[0] #Indeed only accepts one, pick the first provided
        
        if filters.get("remote"):
            params["remotejob"] = "1"
        
        if filters.get("company"):
            params["q"] += f" company:{filters['company']}"
        
        params = {k: v for k, v in params.items() if v}
        return self.BASE_URL + urlencode(params)
    
    def parse_jobs(self,html):
        soup =BeautifulSoup(html, "html.parser")
        jobs=[]
        for card in soup.find_all("a", {"class":"tapItem"}):
            title_el = card.find("h2", {"class":"jonTitle"})
            company_el = card.find("span", {"data-testid":"company-name"})
            location_el = card.find("div", {"data-testid":"text-location"})
            summary_el = card.find("div", {"class":"job-snippet"})
            job={
                "title": title_el.text.strip() if title_el else "",
                "comapany": company_el.text.strip() if company_el else "",
                "location": location_el.text.strip() if location_el else "",
                "summary": summary_el.text.strip() if summary_el else "",
                "url": "https://in.indeed.com" + card.get("href") if card.get("href") else ""
            }
            jobs.append(job)
        return jobs