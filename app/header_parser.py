from urllib.parse import urlparse

# You can define your own "trusted" email domains
TRUSTED_DOMAINS = ["company.com", "gmail.com", "outlook.com", "yahoo.com"]

def extract_domain(email):
    return email.split("@")[-1].lower() if "@" in email else ""

def header_analysis(from_email, to_email, reply_to):
    analysis = {}

    if reply_to and reply_to != from_email:
        analysis["reply_to_mismatch"] = True
    else:
        analysis["reply_to_mismatch"] = False

    domain_from = from_email.split("@")[-1]
    domain_to = to_email.split("@")[-1]

    analysis["same_org"] = domain_from == domain_to

    # Add SPF/DKIM/BIMI simulation
    analysis.update(simulate_spf_dkim_bimi(from_email))

    return analysis


def simulate_spf_dkim_bimi(from_email: str) -> dict:
    domain = from_email.split('@')[-1].lower()
    spf_pass = not any(char.isdigit() for char in domain)
    dkim_pass = domain.count('.') >= 2
    bimi_pass = any(word in domain for word in ['secure', 'auth', 'verified'])

    return {
        "SPF Pass": spf_pass,
        "DKIM Valid": dkim_pass,
        "BIMI Logo Present": bimi_pass
    }


