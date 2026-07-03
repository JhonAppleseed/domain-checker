import socket
from urllib.parse import urlparse

async def dns_lookup_func(domain):
    try:
        domain = domain.strip()
        parsed = urlparse(domain if "://" in domain else f"https://{domain}")
        host = parsed.netloc
        ip_address = socket.gethostbyname(host)
        return {host: ip_address}
    except socket.gaierror as e:
        return {"error": f"Failed to search {domain}, cause {str(e)}"}
