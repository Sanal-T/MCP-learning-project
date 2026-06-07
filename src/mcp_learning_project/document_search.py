"""Small, bounded keyword search over the project's known Markdown documents."""

import re

from .config import (
    DEFAULT_SEARCH_RESULTS,
    DOCUMENTS_DIRECTORY,
    MAX_QUERY_LENGTH,
    MAX_SEARCH_RESULTS,
    MAX_SNIPPET_LENGTH,
)


def _words(text: str) -> list[str]:
    """Split text into case-insensitive alphanumeric terms."""
    return re.findall(r"[a-z0-9]+", text.casefold())


def _snippet(text: str, terms: set[str]) -> str:
    """Choose the best paragraph and clip it to the configured size."""
    paragraphs = [" ".join(part.split()) for part in re.split(r"\n\s*\n", text)]
    paragraphs = [paragraph for paragraph in paragraphs if paragraph]
    if not paragraphs:
        return ""

    best = max(paragraphs, key=lambda paragraph: sum(_words(paragraph).count(term) for term in terms))
    if len(best) <= MAX_SNIPPET_LENGTH:
        return best

    shortened = best[: MAX_SNIPPET_LENGTH - 1].rsplit(" ", 1)[0]
    return f"{shortened}…"


def search_documents(
    query: str, limit: int = DEFAULT_SEARCH_RESULTS
) -> list[dict[str, str]]:
    """Return short matches from known local documents, best matches first.

    A document matches when it contains at least one whole query term. Search
    reads only Markdown files in the configured documents directory. Document
    text is treated as data and is never interpreted as an instruction.
    """
    if not isinstance(query, str):
        raise ValueError("query must be a string")
    if len(query) > MAX_QUERY_LENGTH or len(query.strip()) < 2:
        raise ValueError(f"query must contain 2 to {MAX_QUERY_LENGTH} non-whitespace characters")
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= MAX_SEARCH_RESULTS:
        raise ValueError(f"limit must be an integer from 1 to {MAX_SEARCH_RESULTS}")

    terms = set(_words(query))
    if not terms or not DOCUMENTS_DIRECTORY.is_dir():
        return []

    matches: list[tuple[int, str, str]] = []
    for path in sorted(DOCUMENTS_DIRECTORY.glob("*.md")):
        try:
            content = path.read_text(encoding="utf-8")
        except OSError as error:
            raise RuntimeError(f"Could not read project document: {path.name}") from error

        content_words = _words(content)
        score = sum(content_words.count(term) for term in terms)
        if score:
            matches.append((score, path.name, _snippet(content, terms)))

    matches.sort(key=lambda match: (-match[0], match[1].casefold()))
    return [
        {"document_name": name, "snippet": snippet}
        for _, name, snippet in matches[:limit]
    ]
