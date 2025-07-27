import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

class SimpleCrawler:
    def __init__(self, seeds, delay=1.0, max_pages=100, relevant_keywords=None):
        self.seeds = seeds if isinstance(seeds, list) else [seeds]
        self.visited = set()
        self.to_visit = list(self.seeds)
        self.delay = delay
        self.max_pages = max_pages
        self.discovered = []
        # Only crawl URLs containing these keywords (case-insensitive)
        if relevant_keywords is None:
            self.relevant_keywords = [
                "contact", "about", "team", "company", "leadership", "who-we-are", "our-story", "mission", "vision", "history", "management", "founder", "people", "staff", "careers", "jobs", "partners", "press", "media", "investors", "board"
            ]
        else:
            self.relevant_keywords = [k.lower() for k in relevant_keywords]

    def crawl(self):
        pages_crawled = 0
        while self.to_visit and pages_crawled < self.max_pages:
            url = self.to_visit.pop(0)
            if url in self.visited:
                continue
            print(f"Crawling: {url}")
            try:
                resp = requests.get(url, timeout=10)
                resp.raise_for_status()
            except Exception as e:
                print(f"Failed to fetch {url}: {e}")
                continue
            self.visited.add(url)
            self.discovered.append(url)
            soup = BeautifulSoup(resp.text, 'html.parser')
            # Discover new URLs
            from bs4.element import Tag
            for a in soup.find_all('a', href=True):
                if not isinstance(a, Tag):
                    continue
                href = a.get('href')
                if not isinstance(href, str):
                    continue
                link = urljoin(url, href)
                # Only add if link contains a relevant keyword
                if self._is_valid_url(link) and link not in self.visited and link not in self.to_visit:
                    if any(keyword in link.lower() for keyword in self.relevant_keywords):
                        self.to_visit.append(link)
            # Pagination: look for rel="next" or next-like anchors
            next_link = self._find_next_link(soup, url)
            if next_link and next_link not in self.visited and next_link not in self.to_visit:
                self.to_visit.append(next_link)
            pages_crawled += 1
            time.sleep(self.delay)
        return self.discovered

    def _is_valid_url(self, url):
        parsed = urlparse(url)
        return parsed.scheme in ('http', 'https')

    def _find_next_link(self, soup, base_url):
        # rel="next"
        next_a = soup.find('a', rel=lambda x: x and 'next' in x)
        if next_a and next_a.get('href'):
            return urljoin(base_url, next_a['href'])
        # Common next text
        for text in ['next', 'older', '>>', '›']:
            a = soup.find('a', string=lambda s: s and text in s.lower())
            if a and a.get('href'):
                return urljoin(base_url, a['href'])
        return None

# Example usage:
# crawler = SimpleCrawler(['https://example.com/listing'])
# all_urls = crawler.crawl()
# print(all_urls)
