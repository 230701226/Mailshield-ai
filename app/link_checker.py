import re

# Common risky domains or patterns
RISKY_PATTERNS = [
    r"bit\.ly", r"tinyurl\.com", r"is\.gd",               # URL shorteners
    r"[a-zA-Z]*\d+[a-zA-Z]*\.(com|net|org)",               # suspicious mix of letters/digits
    r"login-[a-z0-9]+\.(com|net)",                         # fake login subdomains
    r"secure-\w+\.(info|xyz|click)",                       # secure-* in sketchy domains
    r"(g00gle|paypa1|1drive|yaho0|faceb00k)\.com"          # common misspelled domains
]

def extract_links(text):
    # Extract all http/https links from body
    return re.findall(r'https?://[^\s]+', text)

def is_suspicious(link):
    # Check against risky patterns
    for pattern in RISKY_PATTERNS:
        if re.search(pattern, link.lower()):
            return True
    return False

def analyze_links(body):
    links = extract_links(body)
    flagged = [link for link in links if is_suspicious(link)]
    return {
        "total_links": len(links),
        "suspicious_links": flagged
    }
