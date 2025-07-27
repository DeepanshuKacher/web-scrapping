import csv
import json
from duckduckgo_search import DDGS

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"
PHONE_REGEX = r"\\+?\\d[\\d\\s().-]{7,}\\d"


def search_query_to_urls(query, max_results=5):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            if r.get("href"):
                results.append(r["href"])
    return results


def save_as_csv(data, filename="output.csv"):
    fieldnames = set()
    for row in data:
        fieldnames.update(row.keys())
    fieldnames = sorted(fieldnames)

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            flat_row = {k: ", ".join(v) if isinstance(v, list) else v for k, v in row.items()}
            writer.writerow(flat_row)
    print(f"[INFO] Data saved to {filename}")
    return filename


def save_as_json(data, filename="output.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[INFO] Data saved to {filename}")
    return json.dumps(data, ensure_ascii=False, indent=2)
