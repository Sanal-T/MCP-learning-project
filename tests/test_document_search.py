"""Checks for the plain Python local document search function."""

import pytest

from mcp_learning_project import document_search


@pytest.fixture
def document_folder(tmp_path, monkeypatch):
    folder = tmp_path / "documents"
    folder.mkdir()
    (folder / "support_policy.md").write_text(
        "# Returns\n\nItems may be returned within 30 days in good condition.",
        encoding="utf-8",
    )
    (folder / "product_faq.md").write_text(
        "# Notebook\n\nThe Field Notebook has 120 pages.", encoding="utf-8"
    )
    (folder / "ignored.txt").write_text("return window", encoding="utf-8")
    monkeypatch.setattr(document_search, "DOCUMENTS_DIRECTORY", folder)
    return folder


def test_search_documents_finds_matching_markdown(document_folder):
    results = document_search.search_documents("RETURNED 30")

    assert results[0]["document_name"] == "support_policy.md"
    assert "30 days" in results[0]["snippet"]
    assert all(result["document_name"].endswith(".md") for result in results)


def test_search_documents_normalizes_punctuation(document_folder):
    results = document_search.search_documents("good-condition!!!")

    assert results[0]["document_name"] == "support_policy.md"


def test_search_documents_returns_empty_list_for_no_match(document_folder):
    assert document_search.search_documents("volcano") == []


def test_search_documents_obeys_result_limit(document_folder):
    results = document_search.search_documents("the", limit=1)

    assert len(results) == 1


@pytest.mark.parametrize("query", ["", " ", "x", "q" * 301, None, 42])
def test_search_documents_rejects_invalid_queries(document_folder, query):
    with pytest.raises(ValueError):
        document_search.search_documents(query)


@pytest.mark.parametrize("limit", [0, 6, True, 1.5, "2"])
def test_search_documents_rejects_invalid_limits(document_folder, limit):
    with pytest.raises(ValueError):
        document_search.search_documents("returns", limit=limit)


def test_search_documents_returns_empty_list_when_folder_is_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(document_search, "DOCUMENTS_DIRECTORY", tmp_path / "missing")

    assert document_search.search_documents("returns") == []


def test_search_documents_keeps_snippets_within_limit(document_folder, monkeypatch):
    monkeypatch.setattr(document_search, "MAX_SNIPPET_LENGTH", 40)
    (document_folder / "long.md").write_text("return " + "useful " * 20, encoding="utf-8")

    result = next(
        item for item in document_search.search_documents("useful")
        if item["document_name"] == "long.md"
    )
    assert len(result["snippet"]) <= 40
