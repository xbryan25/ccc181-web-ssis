from dataclasses import dataclass

from werkzeug.security import check_password_hash

@dataclass
class User:
    user_id: str
    username: str
    email: str
    password_hash: str
    
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
    