import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse

class CompanyInfoExtractor:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def find_about_page_urls(self, base_url):
        """Find potential about page URLs"""
        response = requests.get(base_url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        about_keywords = ['about', 'company', 'who-we-are', 'our-story', 'overview']
        about_urls = []
        
        nav_links = soup.find_all('a', href=True)
        
        for link in nav_links:
            href = link.get('href')
            text = link.get_text().lower()
            
            if any(keyword in text or keyword in href.lower() for keyword in about_keywords):
                full_url = urljoin(base_url, href)
                about_urls.append(full_url)
        
        return about_urls
    
    def extract_company_info(self, url):
        """Extract company information from URL"""
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            for script in soup(["script", "style"]):
                script.extract()
            about_content = self._find_about_content(soup)
            
            if about_content:
                return {
                    'url': url,
                    'about_text': about_content,
                    'word_count': len(about_content.split())
                }
            
            return None
            
        except Exception as e:
            print(f"Error extracting from {url}: {e}")
            return None
    
    def _find_about_content(self, soup):
        """Find about content using multiple strategies"""
        selectors = [
            'section[class*="about"]',
            'div[class*="about"]',
            '[id*="about"]',
            'section[class*="company"]',
            'div[class*="overview"]',
            '.company-description',
            '.about-us',
            '.our-story'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                text = ' '.join([elem.get_text(strip=True) for elem in elements])
                if len(text) > 200:
                    return text
        
        main_selectors = ['main', '[role="main"]', '.main-content', '#main']
        
        for selector in main_selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                if len(text) > 200:
                    return text
        
        body = soup.find('body')
        if body:
            for elem in body.find_all(['nav', 'header', 'footer', '.navigation']):
                elem.extract()
            
            text = body.get_text(strip=True)
            return text  
        
        return None
