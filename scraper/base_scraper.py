# scraper/base_scraper.py
from abc import ABC, abstractmethod
import asyncio
from playwright.async_api import async_playwright

class BaseScrapper(ABC):
    def __init__(self, rate_limit=2, headless=True):
        self.rate_limit=rate_limit
        self.headless=headless

    async def fetch(self, url):
        # async with async_playwright() as p:
        #     browser = await p.chromium.launch(headless=self.headless)
        #     context = await browser.new_context()
        #     page = await context.new_page()
        #     await page.goto(url, wait_until='networkidle')
        #     html =await page.content()
        #     await browser.close()
        # return html
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, args=[
                '--disable-blink-features=AutomationControlled'
            ])
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                locale='en-US',
                ignore_https_errors=True,
            )
            
            await context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            """)
            
            page = await context.new_page()
            await page.goto('https://www.naukri.com', wait_until='networkidle')
            
            # Optionally wait extra for page readiness or to get cookies set
            await page.wait_for_timeout(3000)
            
            await page.goto(url, wait_until='networkidle')
            try:
                await page.wait_for_selector('div.jobTuple', timeout=15000)
            except Exception:
                print("Job list not found, might be blocked or selector changed")
            
            html = await page.content()
            await browser.close()
            return html

    
    @abstractmethod
    def build_url(self,filters):
        pass

    @abstractmethod
    def parse_jobs(self, html):
        pass

    async def scrape(self, filters):
        url = self.build_url(filters)
        html = await self.fetch(url)
        print(html)
        return self.parse_jobs(html)