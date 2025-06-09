from typing import Protocol, Optional
import json
import os
from rep import UserRepositoryProtocol
from User import User


class AuthServiceProtocol(Protocol):
    def sign_in(self, login: str, password: str) -> bool:
        ...

    def sign_out(self) -> None:
        ...

    @property
    def is_authorized(self) -> bool:
        ...

    @property
    def current_user(self) -> Optional[User]:
        ...


class AuthService:
    def __init__(self, user_repo: UserRepositoryProtocol, session_file: str = r"session_file.json"):
        self._user_repo = user_repo
        self._session_file = session_file
        self._current_user: Optional[User] = None
        self._load_session()

    def _load_session(self) -> None:
        if not os.path.exists(self._session_file):
            return
        try:
            with open(self._session_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                user_id = data.get('user_id')
                if user_id is not None:
                    self._current_user = self._user_repo.get_by_id(user_id)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка при загрузке сессии: {e}")
            self._current_user = None

    def _save_session(self) -> None:
        if self._current_user is None:
            return
        try:
            with open(self._session_file, 'w', encoding='utf-8') as file:
                json.dump({'user_id': self._current_user.id}, file)
        except IOError as e:
            print(f"Ошибка при сохранении сессии: {e}")

    def _clear_session_file(self) -> None:
        try:
            if os.path.isfile(self._session_file):
                os.remove(self._session_file)
        except OSError as e:
            print(f"Ошибка при удалении файла сессии: {e}")

    def sign_in(self, login: str, password: str) -> bool:
        user = self._user_repo.get_by_login(login)
        if user and user.password == password:
            self._current_user = user
            self._save_session()
            return True
        return False

    def sign_out(self) -> None:
        self._current_user = None
        self._clear_session_file()

    @property
    def is_authorized(self) -> bool:
        return self._current_user is not None

    @property
    def current_user(self) -> Optional[User]:
        return self._current_user
