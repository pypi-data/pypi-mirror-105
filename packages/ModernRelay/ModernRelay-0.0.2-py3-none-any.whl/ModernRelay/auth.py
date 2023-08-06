import logging
import sqlite3
from pathlib import Path
from typing import Tuple, Union

from aiosmtpd.smtp import AuthResult, LoginPassword, SMTP, Session, Envelope
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class Authenticator:
    def __init__(self, auth_database: Union[str, Path]):
        if isinstance(auth_database, str):
            self.auth_db = Path(auth_database)
        elif isinstance(auth_database, Path):
            self.auth_db = auth_database
        self.ph = PasswordHasher()
        self.logger = logging.getLogger("ModernRelay.log")

    def __call__(self,
                 server: SMTP,
                 session: Session,
                 envelope: Envelope,
                 mechanism: str,
                 auth_data: Tuple[bytes, bytes],
                 ) -> AuthResult:
        fail_nothandled = AuthResult(success=False, handled=False)
        if mechanism not in ("LOGIN", "PLAIN"):
            return fail_nothandled
        if not isinstance(auth_data, LoginPassword):
            return fail_nothandled
        username = auth_data.login.decode('utf-8')
        password = auth_data.password.decode('utf-8')

        conn = sqlite3.connect(str(self.auth_db))
        curs = conn.execute(
            "SELECT hashpass FROM userauth WHERE username=?", (username,)
        )
        hash_db = curs.fetchone()
        conn.close()
        if not hash_db:
            return fail_nothandled
        try:
            if self.ph.verify(hash_db[0], password):
                self.logger.info(f"User {username} authenticated")
                return AuthResult(success=True)
        except VerifyMismatchError:
            self.logger.warning(f"User {username} failed authentication!")

        return fail_nothandled
