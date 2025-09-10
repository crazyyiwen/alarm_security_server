import os
from dotenv import load_dotenv

def set_env():
    """Load OPENAI_API_KEY from .env and environment."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Please define it in your .env or environment.")
    else:
        os.environ["OPENAI_API_KEY"] = api_key