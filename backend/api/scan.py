from backend.models import ScanRequest
from fastapi import APIRouter
from backend.tools.dns_lookup import dns_lookup_func
from backend.tools.security_headers import analyze_headers_func
from backend.tools.whois_tool import whois_tool_func
from backend.tools.port_scan import port_scan_func

import asyncio

tool_func = {
    "dns": dns_lookup_func,
    "seched": analyze_headers_func,
    "whois": whois_tool_func,
    # "tls": tls_func,
    "ports": port_scan_func,
    # "techdet": tech_detection_func,
}

router = APIRouter(prefix="/api")

@router.post("/scan")
async def scanURL(req: ScanRequest): #must be async with multiple functions
    tasks = {
        check: tool_func[check](req.domain)
        for check in req.checks
        if check in tool_func
    }

    results = await asyncio.gather(*tasks.values())
    
    response = {
        name: result
        for name, result in zip(tasks.keys(), results)
    }


    return {'result': response}