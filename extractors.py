import re

TECH_KEYWORDS = [
    "React", "Next.js", "Angular", "Vue", "Tailwind", "Bootstrap", "Node.js",
    "Django", "Flask", "Laravel", "Spring", "GraphQL", "MongoDB",
    "PostgreSQL", "MySQL", "Redis", "Firebase", "AWS", "Azure", "GCP"
]

def extract_tech_stack(text):
    return [tech for tech in TECH_KEYWORDS if re.search(rf"\\b{re.escape(tech)}\\b", text, re.IGNORECASE)]

def extract_focus_areas(text):
    matches = re.findall(r"(currently working on.*?|recent projects.*?|new (product|launch).*?\.)", text, re.IGNORECASE)
    return [m[0] for m in matches] if matches else []

def extract_competitors(text):
    competitors = re.findall(r"(alternative to|compared to|vs\\.?)\\s+([A-Za-z0-9\\s&\-]+)", text, re.IGNORECASE)
    return [comp[1].strip() for comp in competitors]

def extract_positioning(text):
    phrases = re.findall(r"(market leader|leading provider|#1 in|top \\d+|pioneer in)", text, re.IGNORECASE)
    return list(set(phrases))
