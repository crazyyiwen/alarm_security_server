import os

from dotenv import load_dotenv

def set_env():
    """Load OPENAI_API_KEY from .env and environment."""
    load_dotenv()
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    api_key = os.getenv("OPENAI_API_KEY")
    if os.getenv("LANGCHAIN_API_KEY"):
        print("LangSmith tracing enabled")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Please define it in your .env or environment.")
    else:
        os.environ["OPENAI_API_KEY"] = api_key