# who is tool
import whois

async def whois_tool_func(domain):
    try:
        domain = domain.strip()
        if not domain.startswith(("http://", "https://")):
            domain = "https://" + domain
        response = whois.whois(domain)
        return response
    except whois.exceptions.WhoisError as e:
        return {'error': f"Failed to connect: {str(e)} "}



