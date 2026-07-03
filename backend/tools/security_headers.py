# security headers
import requests

async def analyze_headers_func(domain):
    try:
        domain = domain.strip()
        if not domain.startswith(("http://", "https://")):
            domain = "https://" + domain

        response = requests.head(domain, timeout=5, allow_redirects=True)

        return dict(response.headers)

    except requests.exceptions.RequestException as e:
        return {"error", f"Failed to connect: {str(e)}"}