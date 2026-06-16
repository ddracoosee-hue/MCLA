import base64
import os
from openai import OpenAI
from schemas.data_models import NetworkTopology

# Initialize client; automatically picks up OPENAI_API_KEY from environment
client = OpenAI()

def encode_image_to_base64(image_path: str) -> str:
    """
    Reads a local image file and converts it to a base64 encoded string.
    Supports standard image formats (PNG, JPEG, WebP).
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Target topology image not found at: {image_path}")
        
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_topology(image_path: str) -> NetworkTopology:
    """
    Ingests a network diagram image, transmits it to GPT-4o, and maps the 
    visual layout directly into a deterministic NetworkTopology Pydantic object.
    """
    # 1. Convert visual data to an absolute data stream
    base64_image = encode_image_to_base64(image_path)
    
    # 2. System prompt acting as the operational directive for spatial parsing
    system_instruction = (
        "You are an expert infrastructure auditor. Analyze the provided network topology diagram. "
        "Identify all structural components (firewalls, routers, subnets, servers, databases) as Nodes. "
        "Identify all explicit connections, directional vectors, or allowed pathways between them as AllowedConnections. "
        "Extract details with strict accuracy. If an element or IP range is explicitly labeled, include it."
    )

    # 3. Execute type-safe multimodal analysis
    # We use the beta.chat.completions.parse engine to guarantee Pydantic schema compliance
    parsed_completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": system_instruction
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": "Parse this network topology diagram into the mandated structural JSON format."
                    },
                    {
                        "type": "image_url", 
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                ]
            }
        ],
        response_format=NetworkTopology,
    )
    
    # 4. Extract the cleanly instantiated data model
    topology_data = parsed_completion.choices[0].message.parsed
    
    if not topology_data:
        raise ValueError("Failed to extract valid structural data from the provided network diagram.")
        
    return topology_data