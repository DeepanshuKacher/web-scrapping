import re
import requests
from bs4 import BeautifulSoup
from extractors import extract_tech_stack, extract_focus_areas, extract_competitors, extract_positioning
from utils import search_query_to_urls
from crawler import SimpleCrawler

SOCIAL_PATTERNS = {
    "LinkedIn": r"(https://[a-z]*\\.?linkedin\\.com/[^\"'<> )]+)",
    "Twitter": r"(https://[a-z]*\\.?twitter\\.com/[^\"'<> )]+)",
    "Facebook": r"(https://[a-z]*\\.?facebook\\.com/[^\"'<> )]+)",
    "Instagram": r"(https://[a-z]*\\.?instagram\\.com/[^\"'<> )]+)"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"
PHONE_REGEX = r"\\+?\\d[\\d\\s().-]{7,}\\d"

def extract_info_from_url(url, level="basic"):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ')

        # Robust extraction of title
        if soup.title and hasattr(soup.title, 'string') and soup.title.string:
            company_name = soup.title.string.strip()
        else:
            company_name = "N/A"
        data = {
            "Company Name": company_name,
            "Website": url,
            "Emails": list(set(re.findall(EMAIL_REGEX, text))),
            "Phone Numbers": list(set(re.findall(PHONE_REGEX, text))),
        }

        if level in ["medium", "advanced"]:
            for platform, pattern in SOCIAL_PATTERNS.items():
                matches = re.findall(pattern, response.text)
                data[platform] = list(set(matches))

            address_tag = soup.find('address')
            if address_tag:
                data["Address"] = address_tag.get_text(strip=True)
            else:
                address_keywords = re.findall(r'\\d{1,5}\\s+\\w+(\\s\\w+)*,\\s*\\w+(\\s\\w+)*,\\s*\\w{2,3}\\s*\\d{5}', text)
                data["Address"] = address_keywords[0] if address_keywords else "N/A"

            from bs4.element import Tag
            description = soup.find("meta", attrs={"name": "description"}) or \
                          soup.find("meta", attrs={"property": "og:description"})
            desc_content = None
            if isinstance(description, Tag):
                desc_content = description.get("content")
            data["Tagline / Description"] = desc_content.strip() if isinstance(desc_content, str) else "N/A"

            founded_match = re.search(r"(Founded|Since)\\s+(\\d{4})", text, re.IGNORECASE)
            data["Year Founded"] = founded_match.group(2) if founded_match else "N/A"

            keywords = soup.find("meta", attrs={"name": "keywords"})
            keywords_content = None
            if isinstance(keywords, Tag):
                keywords_content = keywords.get("content")
            data["Products/Services"] = keywords_content.strip() if isinstance(keywords_content, str) else "N/A"

            industry_match = re.search(r"Industry[:\-]?\\s*([A-Za-z ,&]+)", text, re.IGNORECASE)
            data["Industry/Sector"] = industry_match.group(1).strip() if industry_match else "N/A"

        if level == "advanced":
            data["Tech Stack"] = extract_tech_stack(text)
            data["Current Projects"] = extract_focus_areas(text)
            data["Competitors"] = extract_competitors(text)
            data["Market Positioning"] = extract_positioning(text)

        return data

    except Exception as e:
        print(f"[ERROR] Failed to scrape {url}: {e}")
        return None

def scrape_from_queries(queries, level):
    all_data = []
    for query in queries:
        print(f"[INFO] Searching for: {query}")
        urls = search_query_to_urls(query)
        for url in urls:
            print(f"  > Scraping {url}")
            data = extract_info_from_url(url, level)
            if data:
                all_data.append(data)
    return all_data

def scrape_from_seed_urls(seed_urls, level):
    all_data = []
    # Use SimpleCrawler to discover all relevant URLs from the seeds
    crawler = SimpleCrawler(seed_urls)
    discovered_urls = crawler.crawl()
    print(f"[INFO] Discovered {len(discovered_urls)} URLs from seeds.")
    for url in discovered_urls:
        print(f"  > Scraping {url}")
        data = extract_info_from_url(url, level)
        if data:
            all_data.append(data)
    return all_data
