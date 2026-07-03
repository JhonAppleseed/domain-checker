import subprocess
import re

target = "109.71.185.39"

async def port_scan_func(domain):
    try:
        result = subprocess.run([
            r"C:\Program Files (x86)\Nmap\nmap.exe",
            'nmap', 
            '-sS', 
            '-p', 
            '1-1000', 
            domain], capture_output=True, text=True)
        
        result_array = result.stdout.split("\n")
        parsed = parse_nmap_output(result_array)
        return parsed
    except TimeoutError as e:
        return {'error': f'Connection timed out {str(e)}'}
    except e:
        return {'error': f'Problem: {str(e)}'}

def parse_nmap_output(lines):
    result = {
        "scanner": None,
        "scan_time": None,
        "host": None,
        "ip": None,
        "rdns": None,
        "host_up": False,
        "latency": None,
        "closed_ports": None,
        "ports": [],
        "scan_duration": None,
    }

    port_pattern = re.compile(r"(\d+)/tcp\s+(\w+)\s+(.+)")

    for line in lines:
        line = line.strip()

        if line.startswith("Starting Nmap"):
            result["scanner"] = line.split(" at ")[0]
            result["scan_time"] = line.split(" at ")[1]

        elif line.startswith("Nmap scan report for"):
            match = re.search(r"Nmap scan report for (.+?) \(([\d.]+)\)", line)
            if match:
                result["host"] = match.group(1)
                result["ip"] = match.group(2)

        elif line.startswith("Host is up"):
            result["host_up"] = True
            latency = re.search(r"\((.*?) latency\)", line)
            if latency:
                result["latency"] = latency.group(1)

        elif line.startswith("rDNS record for"):
            result["rdns"] = line.split(": ", 1)[1]

        elif line.startswith("Not shown:"):
            result["closed_ports"] = line

        elif "/tcp" in line:
            match = port_pattern.match(line)
            if match:
                result["ports"].append({
                    "port": int(match.group(1)),
                    "protocol": "tcp",
                    "state": match.group(2),
                    "service": match.group(3)
                })

        elif line.startswith("Nmap done:"):
            duration = re.search(r"scanned in (.+)", line)
            if duration:
                result["scan_duration"] = duration.group(1)

    return result
