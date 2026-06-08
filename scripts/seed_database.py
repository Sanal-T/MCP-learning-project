"""Create the local sample product database with fictional records."""

from pathlib import Path
import sqlite3


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_PATH = PROJECT_ROOT / "data" / "sample.db"

PRODUCTS = (
    ("PROD-001", "Trail Bottle", "Accessories", 1800, 1, "A reusable 750 ml bottle."),
    ("PROD-002", "Desk Lamp", "Office", 3200, 1, "A desk lamp with three brightness settings."),
    ("PROD-003", "Field Notebook", "Stationery", 900, 1, "A pocket notebook with 120 pages."),
    ("PROD-004", "Canvas Tote", "Accessories", 1400, 0, "A lightweight everyday carry bag."),
    ("PROD-005", "Cable Organizer", "Office", 700, 1, "A small organizer for charging cables."),
    ("PROD-006", "Reading Stand", "Office", 2400, 1, "An adjustable stand for books and tablets."),
    ("PROD-007", "Welcome Kit", "Bundles", 2600, 0, "A notebook, reusable bottle, and quick-start card."),
    ("PROD-008", "Travel Mug", "Accessories", 2100, 1, "An insulated mug for hot or cold drinks."),
)


def seed_database() -> Path:
    """Create or replace the sample products table and return its path."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("DROP TABLE IF EXISTS products")
        connection.execute(
            """
            CREATE TABLE products (
                product_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price_cents INTEGER NOT NULL CHECK (price_cents >= 0),
                in_stock INTEGER NOT NULL CHECK (in_stock IN (0, 1)),
                description TEXT NOT NULL
            )
            """
        )
        connection.executemany(
            """
            INSERT INTO products
                (product_id, name, category, price_cents, in_stock, description)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            PRODUCTS,
        )

    return DATABASE_PATH


if __name__ == "__main__":
    database_path = seed_database()
    print(f"Created sample database with {len(PRODUCTS)} products: {database_path}")
