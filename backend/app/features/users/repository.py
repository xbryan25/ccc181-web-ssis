from app.db.queries.common import CommonQueries

from flask import current_app

class UserRepository:

    @staticmethod
    def get_user_by_email(email: str) -> dict | None:
        db = current_app.extensions['db']

        return db.fetch_one(CommonQueries.GET_BY_SPECIFIC_COLUMN.format(table="users", column="email"), (email, ))

    @staticmethod
    def user_signup(user_id, username, email, password_hash):
        db = current_app.extensions['db']

        db.execute_query(CommonQueries.INSERT.format(table="users", 
                                                     columns="user_id, username, email, password_hash",
                                                     placeholders="%s, %s, %s, %s"),
                                                     (user_id, username, email, password_hash))
        
    @staticmethod
    def get_username(user_id):
        db = current_app.extensions['db']

        return db.fetch_one(CommonQueries.GET_COLUMN_BY_PK.format(column="username", table="users", pk="user_id"), (user_id, ))
        