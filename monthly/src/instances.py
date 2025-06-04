# Parse config.yml
from dotenv import load_dotenv
from pyaml_env import parse_config
load_dotenv()
config = parse_config('config.yml', encoding = 'utf-8')


# Load logger
from .logger import get_logger
logger = get_logger()
logger.info('Logging timestamps are respect to America/Lima timezone')