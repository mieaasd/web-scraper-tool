import requests
from bs4 import BeautifulSoup
import re

class EcommerceScraper:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    def scrape(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            products = soup.find_all(['div', 'article'], class_=re.compile(r'product|item', re.I))
            for product in products[:50]:
                try:
                    name_elem = product.find(['h2', 'h3', 'a'], class_=re.compile(r'name|title', re.I))
                    name = name_elem.get_text(strip=True) if name_elem else 'N/A'
                    price_elem = product.find(['span', 'div'], class_=re.compile(r'price|cost', re.I))
                    price = price_elem.get_text(strip=True) if price_elem else 'N/A'
                    if name != 'N/A':
                        results.append({'Product Name': name[:100], 'Price': price})
                except:
                    pass
            return results
        except:
            return []