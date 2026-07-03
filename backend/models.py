from pydantic import BaseModel

class ScanRequest(BaseModel):
    domain: str
    checks: list[str]