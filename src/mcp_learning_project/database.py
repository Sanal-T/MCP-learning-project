"""Read-only access to the fictional sample product database."""

import sqlite3

from .config import DATABASE_PATH


def get_product(product_id: str) -> dict[str, str | int] | None:
    """Return one product by exact ID, or ``None`` when it does not exist.

    The database file is opened in read-only mode. The caller cannot choose a
    database path, and the ID is passed as a SQL parameter rather than inserted
    into the query text.
    """
    if not isinstance(product_id, str):
        raise ValueError("product_id must be a string")
    if not product_id.strip() or len(product_id) > 32:
        raise ValueError("product_id must contain 1 to 32 non-whitespace characters")

    if not DATABASE_PATH.is_file():
        raise FileNotFoundError(
            "Sample database is missing. Create it by running: "
            "python scripts/seed_database.py"
        )

    database_uri = f"{DATABASE_PATH.as_uri()}?mode=ro"
    with sqlite3.connect(database_uri, uri=True) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            """
            SELECT product_id, name, category, price_cents, in_stock, description
            FROM products
            WHERE product_id = ?
            """,
            (product_id,),
        ).fetchone()

    if row is None:
        return None
    return dict(row)
