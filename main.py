# main.py
import asyncio
from filters import merge_filters
from scraper.indeed_scraper import IndeedScraper
from scraper.naukri_scraper import NaukriScraper

user_input = {
    "keywords": input("Enter keywords (e.g. Data Analyst): ") or "",
    "location": input("Enter location (e.g. Bangalore): ") or "",
    "date_posted": input("Enter date posted (any, 1, 3, 7, 14): ") or "any",
    "job_type": [input("Job type (fulltime/parttime/contract/internship/leave blank for all): ")] if input("Specify job type? (y/n): ").strip().lower() == "y" else [],
    "company": input("Enter company name (optional): ") or "",
    "remote": input("Remote only? (y/n): ").lower() == "y"
}
filters = merge_filters(user_input)

async def run_scrapers():
    # print("\n--- Indeed ---")
    # indeed = IndeedScraper()
    # indeed_jobs = await indeed.scrape(filters)
    # for j in indeed_jobs[:5]:
    #     print(j)

    print("\n--- Naukri ---")
    naukri = NaukriScraper()
    naukri_jobs = await naukri.scrape(filters)
    print(naukri_jobs)
    for j in naukri_jobs[:5]:
        print(j)

if __name__ == "__main__":
    asyncio.run(run_scrapers())