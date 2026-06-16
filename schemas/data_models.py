from pydantic import BaseModel, Field
from typing import List, Optional

class Node(BaseModel):
    id: str = Field(..., description="Unique identifier for the node, e.g., 'FW-01' or 'Web-Tier'")
    device_type: str = Field(..., description="The functional role of the device, e.g., 'Firewall', 'Web Server', 'Database'")
    ip_address: Optional[str] = Field(default=None, description="The IP address, IP range, or CIDR block associated with the node")

class AllowedConnection(BaseModel):
    source_id: str = Field(..., description="The ID of the originating node")
    target_id: str = Field(..., description="The ID of the destination node")
    protocol: str = Field(..., description="Network protocol, e.g., 'TCP', 'UDP', 'HTTP', 'HTTPS', 'SSH'")
    allowed_ports: List[int] = Field(..., description="List of allowed port numbers for this connection")

class NetworkTopology(BaseModel):
    nodes: List[Node] = Field(..., description="List of all identified nodes in the network diagram")
    allowed_connections: List[AllowedConnection] = Field(..., description="List of all permitted communication pathways defined by the diagram")

class LogEvent(BaseModel):
    timestamp: str = Field(..., description="Timestamp of the event")
    source_ip: str = Field(..., description="Source IP address of the traffic")
    target_ip: str = Field(..., description="Destination IP address of the traffic")
    protocol: str = Field(..., description="Protocol used, e.g., 'TCP', 'UDP'")
    port: int = Field(..., description="Destination port number")
    action: str = Field(..., description="Action taken by the logging device, e.g., 'ALLOW', 'DENY', 'DROP'")
    metadata: Optional[str] = Field(default=None, description="Any additional payload or packet details")

class SecurityAnomaly(BaseModel):
    severity: str = Field(..., description="Severity of the anomaly: 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'")
    violating_event: LogEvent = Field(..., description="The specific kinetic log event that triggered the anomaly")
    topological_conflict: str = Field(..., description="Detailed explanation of why this event violates the established static network topology")
    remediation_suggestion: str = Field(..., description="Actionable architectural or firewall rule advice to mitigate the flaw")