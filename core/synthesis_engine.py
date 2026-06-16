from pydantic import BaseModel
from typing import List
from openai import OpenAI
from schemas.data_models import NetworkTopology, LogEvent, SecurityAnomaly, AnomalyReport

client = OpenAI()

def analyze_vulnerabilities(topology: NetworkTopology, logs: List[LogEvent]) -> List[SecurityAnomaly]:
    """
    Synthesizes the static spatial topology with kinetic log telemetry to 
    identify architectural bypasses and security vulnerabilities.
    """
    if not logs:
        print("[*] No log events provided for analysis. Synthesis aborted.")
        return []

    # System instruction framing the LLM as an absolute logical observer
    system_instruction = (
        "You are an elite network security analyzer. You are provided with two absolute datasets:\n"
        "1. The State Space: A strict network topology defining all permitted nodes and allowed connections.\n"
        "2. The Kinetic Reality: A sequential list of executed network traffic logs.\n\n"
        "Your objective is to identify any logical contradictions. An anomaly occurs if:\n"
        "- Traffic bypasses a required security node (e.g., communicating directly with a protected database without traversing a firewall).\n"
        "- Traffic utilizes a protocol or port not explicitly permitted in the topology.\n"
        "- A node that does not exist in the topology map interacts with internal infrastructure.\n\n"
        "Analyze the data deterministically. Return a structured report of all violations."
    )

    # We convert our rigorous Pydantic models into pure JSON strings to feed the context window
    user_payload = f"""
    === PERMITTED STATE SPACE (TOPOLOGY) ===
    {topology.model_dump_json(indent=2)}
    
    === OBSERVED PHENOMENA (LOGS) ===
    {[log.model_dump_json() for log in logs]}
    """

    print("[*] Executing cross-modal cognitive synthesis...")
    
    parsed_completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_payload}
        ],
        response_format=AnomalyReport,
        # Setting temperature to 0.0 forces the model to heavily favor deterministic logic over creative hallucination
        temperature=0.0 
    )

    report = parsed_completion.choices[0].message.parsed
    
    if not report or not report.anomalies:
        return []
        
    return report.anomalies