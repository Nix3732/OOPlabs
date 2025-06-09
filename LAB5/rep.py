from typing import Protocol, Optional, TypeVar, Sequence
import os, json
from User import User


T = TypeVar('T')
ID = "id"
LOGIN = "login"


class DataRepositoryProtocol(Protocol[T]):
    def get_all(self) -> Sequence[T]:
        ...

    def get_by_id(self, id: int) -> Optional[T]:
        ...

    def add(self, item: T):
        ...

    def update(self, item: T):
        ...

    def delete(self, item: T):
        ...


class DataRepository(DataRepositoryProtocol[T]):
    def __init__(self, file_path: str, T):
        self.file_path = file_path
        self.T = T
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        self._data = self._load_data()

    def _load_data(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_data(self):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self._data, file, indent=2)

    def get_all(self) -> Sequence[T]:
        return [self.T(**item) for item in self._data]

    def get_by_id(self, id: int) -> Optional[T]:
        for item in self._data:
            if item[ID] == id:
                return self.T(**item)
        return None

    def add(self, item: T) -> None:
        self._data.append(item.__dict__)
        self._save_data()

    def update(self, item: T) -> None:
        for i, entry in enumerate(self._data):
            if entry[ID] == item.id:
                self._data[i] = item.__dict__
                break
        self._save_data()

    def delete(self, item: T) -> None:
        self._data = [elem for elem in self._data if elem[ID] != item.id]
        self._save_data()


class UserRepositoryProtocol(DataRepositoryProtocol[User], Protocol):
    def get_by_login(self, login: str) -> Optional[User]:
        ...


class UserRepository(DataRepository[User], UserRepositoryProtocol):
    def __init__(self, file_path: str = r"D:\Python Project\OOP3\Users.json"):
        super().__init__(file_path, User)

    def get_by_login(self, login: str) -> Optional[User]:
        for item in self._load_data():
            if item['login'] == login:
                return User(**item)
        return None
