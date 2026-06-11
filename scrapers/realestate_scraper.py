import requests
from bs4 import BeautifulSoup
import re

class RealEstateScraper:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    def scrape(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            properties = soup.find_all(['div', 'article'], class_=re.compile(r'property|listing', re.I))
            for prop in properties[:50]:
                try:
                    title_elem = prop.find(['h2', 'h3', 'a'])
                    title = title_elem.get_text(strip=True) if title_elem else 'N/A'
                    price_elem = prop.find(['span', 'div'], class_=re.compile(r'price|cost|rent', re.I))
                    price = price_elem.get_text(strip=True) if price_elem else 'N/A'
                    if title != 'N/A':
                        results.append({'Title': title[:100], 'Price': price})
                except:
                    pass
            return results
        except:
            return []