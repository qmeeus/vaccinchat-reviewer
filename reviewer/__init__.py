from dotenv import load_dotenv
from pathlib import Path


env_file = Path(__file__).parents[1]/".env"
if not env_file.exists():
    raise FileNotFoundError(f"Missing .env file with credentials and url")
load_dotenv(env_file)

