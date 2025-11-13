from flask import current_app

import psycopg
from psycopg.rows import dict_row, TupleRow, DictRow

from typing import Any

class Database:
    """Singleton class for database connection"""

    _instance = None

    def __new__(cls) -> "Database":
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._connect()
        return cls._instance

    def _connect(self) -> None:
        self.conn = psycopg.connect(
            dbname=current_app.config["DB_NAME"],
            port=current_app.config["DB_PORT"],
            user=current_app.config["DB_USER"],
            password=current_app.config["DB_PASS"],
            host=current_app.config["DB_HOST"],
            row_factory=dict_row # type: ignore[arg-type]
        ) 

    def execute_query(self, query, params=None) -> None:
        """For INSERT, UPDATE, DELETE queries."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def fetch_all(self, query, params=None) -> list[TupleRow]:
        """For SELECT queries returning multiple rows."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchall()
        except Exception as e:
            raise e

    def fetch_one(self, query, params=None) -> TupleRow | None:
        """For SELECT queries returning a single row."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchone()
        except Exception as e:
            raise e

    def close(self) -> None:
        if self.conn:
            self.conn.close()
            Database._instance = None