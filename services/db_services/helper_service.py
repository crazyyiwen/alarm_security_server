import json
import re
from typing import Dict, List


def parse_chat_history(raw_data: str) -> List[Dict[str, str]]:
    """
    Parse chat history from serialized data.
    
    Args:
        raw_data (str): Raw JSON string from database.
    
    Returns:
        List[Dict[str, str]]: Parsed messages with role and content.
    """
    try:
        # Step 1: Load the outer JSON
        data = json.loads(raw_data)
        message_str = data.get("message", "")

        # Step 2: Regex to extract roles and content
        pattern = re.compile(r"(HumanMessage|AIMessage)\(content=(.+?)(?=, additional_kwargs)")
        matches = pattern.findall(message_str)

        parsed = []
        for role, content in matches:
            # Clean content string
            content = content.strip().strip("'").strip('"')
            parsed.append({
                "role": "human" if role == "HumanMessage" else "ai",
                "content": content
            })

        return parsed
    except Exception as e:
        return [{"error": f"Failed to parse: {e}"}]