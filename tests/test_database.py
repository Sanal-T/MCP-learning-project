"""Checks for the plain Python product lookup function."""

import sqlite3

import pytest

from mcp_learning_project import database


@pytest.fixture
def sample_database(tmp_path, monkeypatch):
    """Create a tiny database just for one test."""
    path = tmp_path / "sample.db"
    with sqlite3.connect(path) as connection:
        connection.execute(
            """
            CREATE TABLE products (
                product_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price_cents INTEGER NOT NULL,
                in_stock INTEGER NOT NULL,
                description TEXT NOT NULL
            )
            """
        )
        connection.execute(
            "INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)",
            ("PROD-003", "Field Notebook", "Stationery", 900, 1, "120 pages."),
        )
    monkeypatch.setattr(database, "DATABASE_PATH", path)
    return path


def test_get_product_returns_matching_record(sample_database):
    assert database.get_product("PROD-003") == {
        "product_id": "PROD-003",
        "name": "Field Notebook",
        "category": "Stationery",
        "price_cents": 900,
        "in_stock": 1,
        "description": "120 pages.",
    }


def test_get_product_returns_none_when_id_is_missing(sample_database):
    assert database.get_product("PROD-999") is None


def test_get_product_treats_sql_metacharacters_as_data(sample_database):
    assert database.get_product("' OR 1=1 --") is None


@pytest.mark.parametrize("product_id", ["", "   ", "x" * 33, None, 123])
def test_get_product_rejects_invalid_ids(sample_database, product_id):
    with pytest.raises(ValueError):
        database.get_product(product_id)


def test_get_product_reports_missing_database(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "missing.db")

    with pytest.raises(FileNotFoundError, match="seed_database.py"):
        database.get_product("PROD-003")
