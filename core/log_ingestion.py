import re
import os
from typing import List
from schemas.data_models import LogEvent

def parse_kinetic_logs(log_path: str) -> List[LogEvent]:
    """
    Ingests unstructured text logs (e.g., standard Linux UFW / iptables)
    and maps them deterministically into structured LogEvent objects.
    """
    if not os.path.exists(log_path):
        raise FileNotFoundError(f"Kinetic log file not found at: {log_path}")

    parsed_events = []
    
    # Precision Regex pattern utilizing greedy backtracking for optional port extraction
    log_pattern = re.compile(
        r"(?P<timestamp>[A-Z][a-z]{2}\s+\d+\s+\d{2}:\d{2}:\d{2}).*?"
        r"\[UFW (?P<action>ALLOW|BLOCK|DENY|AUDIT)\].*?"
        r"SRC=(?P<src_ip>\S+).*?"
        r"DST=(?P<dst_ip>\S+).*?"
        r"PROTO=(?P<protocol>\S+)"
        r"(?:.*DPT=(?P<port>\d+))?"  # Greedy search ensures DPT is caught if present
    )

    with open(log_path, 'r') as file:
        for line_number, line in enumerate(file, 1):
            match = log_pattern.search(line)
            if match:
                data = match.groupdict()
                
                try:
                    event = LogEvent(
                        timestamp=data['timestamp'],
                        source_ip=data['src_ip'],
                        target_ip=data['dst_ip'],
                        protocol=data['protocol'],
                        port=int(data['port']) if data['port'] else 0,
                        action=data['action'],
                        metadata=f"Raw Line {line_number}: {line.strip()}"
                    )
                    parsed_events.append(event)
                except ValueError:
                    continue

    return parsed_events