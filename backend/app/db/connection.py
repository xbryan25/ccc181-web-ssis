# app/db/connection.py
import psycopg
from app.config import Db_config

class Database:
    """Singleton class for database connection"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        self.conn = psycopg.connect(
            dbname=Db_config.DB_NAME,
            user=Db_config.DB_USER,
            password=Db_config.DB_PASSWORD,
            host=Db_config.DB_HOST
        )

    def execute_query(self, query, params=None):
        """For INSERT, UPDATE, DELETE queries."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def fetch_all(self, query, params=None):
        """For SELECT queries returning multiple rows."""
        try:
            with self.conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                cur.execute(query, params)
                return cur.fetchall()
        except Exception as e:
            raise e

    def fetch_one(self, query, params=None):
        """For SELECT queries returning a single row."""
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                return cur.fetchone()
        except Exception as e:
            raise e

    def close(self):
        if self.conn:
            self.conn.close()
            Database._instance = None