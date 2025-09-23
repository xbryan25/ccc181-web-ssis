from app.db.queries.common import CommonQueries

from flask import current_app

class UserRepository:

    @staticmethod
    def get_user_by_email(email: str) -> dict | None:
        db = current_app.extensions['db']

        return db.fetch_one(CommonQueries.GET_BY_SPECIFIC_COLUMN.format(table="users", column="email"), (email, ))
