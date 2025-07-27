
# --- Imports from modules ---
from scraper import extract_info_from_url, scrape_from_queries, scrape_from_seed_urls
from utils import save_as_csv, save_as_json
import json


# --- MAIN LOGIC AS FUNCTION ---
def run(input_data: dict):
    """
    input_data example:
    {
        "mode": "query" or "url",
        "scrape_level": "basic"/"medium"/"advanced",
        "queries": ["query1", "query2"],  # if mode == "query"
        "seed_urls": ["url1", "url2"],    # if mode == "url"
        "output_type": "csv" or "json"
    }
    """
    mode = input_data.get("mode", "query").strip().lower()
    scrape_level = input_data.get("scrape_level", "basic").strip().lower()
    output_type = input_data.get("output_type", "json").strip().lower()

    if mode == "query":
        queries = input_data.get("queries")
        if not queries or not isinstance(queries, list):
            return {"error": "'queries' field (list of strings) is required when mode is 'query'."}
        data = scrape_from_queries([q.strip() for q in queries], scrape_level)
    elif mode == "url":
        seed_urls = input_data.get("seed_urls")
        if not seed_urls or not isinstance(seed_urls, list):
            return {"error": "'seed_urls' field (list of strings) is required when mode is 'url'."}
        data = scrape_from_seed_urls([u.strip() for u in seed_urls], scrape_level)
    else:
        return {"error": "Invalid mode."}

    if output_type == "csv":
        save_as_csv(data)
        return {"message": "Data saved as CSV."}
    else:
        save_as_json(data)
        return data

# --- CLI ENTRYPOINT (optional, for backward compatibility) ---
if __name__ == "__main__":
    mode = input("Choose mode (query/url): ").strip().lower()
    scrape_level = input("Scraping level (basic/medium/advanced): ").strip().lower()

    if mode == "query":
        queries = input("Enter search queries separated by commas:\n").split(",")
        data = scrape_from_queries([q.strip() for q in queries], scrape_level)
    elif mode == "url":
        seed_urls = input("Enter URLs separated by commas:\n").split(",")
        data = scrape_from_seed_urls([u.strip() for u in seed_urls], scrape_level)
    else:
        print("Invalid mode.")
        exit()

    output_type = input("Output format (csv/json): ").strip().lower()
    if output_type == "csv":
        save_as_csv(data)
    else:
        save_as_json(data)
        print(json.dumps(data, indent=2, ensure_ascii=False))
