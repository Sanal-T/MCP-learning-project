"""Project paths and safe defaults shared by the retrieval functions."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIRECTORY = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIRECTORY / "sample.db"
DOCUMENTS_DIRECTORY = DATA_DIRECTORY / "documents"

MAX_SEARCH_RESULTS = 5
DEFAULT_SEARCH_RESULTS = 3
MAX_QUERY_LENGTH = 300
MAX_SNIPPET_LENGTH = 240
