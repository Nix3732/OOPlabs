from Protocols import PropertyChangedListenerProtocol, PropertyChangingListenerProtocol
from Protocols import T
from typing import List
from Validators import NameValidator, AgeValidator


class User:
    def __init__(self, name: str, age: int):
        self._name = name
        self._age = age
        self._changed_listeners: List[PropertyChangedListenerProtocol] = []
        self._changing_listeners: List[PropertyChangingListenerProtocol] = []

        temp_validators = [
            NameValidator(),
            AgeValidator()
        ]

        for validator in temp_validators:
            self.add_property_changing_listener(validator)

        if not self._validate_property_change("name", None, name):
            raise ValueError(f"Невозможное значения для создания класса: {name}")

        if not self._validate_property_change("age", None, age):
            raise ValueError(f"Невозможное значения для создания класса: {age}")

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if self._name != value:
            if self._validate_property_change("name", self._name, value):
                self._name = value
                self._notify_property_changed("name")
            else:
                print(f"Проверка имени не пройдена: {value}")

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int):
        if self._age != value:
            if self._validate_property_change("age", self._age, value):
                self._age = value
                self._notify_property_changed("age")
            else:
                print(f"Проверка возраста не пройдена: {value}")

    # Методы для работы с наблюдателями изменений
    def add_property_changed_listener(self, listener: PropertyChangedListenerProtocol):
        if listener not in self._changed_listeners:
            self._changed_listeners.append(listener)

    def remove_property_changed_listener(self, listener: PropertyChangedListenerProtocol):
        if listener in self._changed_listeners:
            self._changed_listeners.remove(listener)

    def _notify_property_changed(self, property_name: str):
        for listener in self._changed_listeners:
            listener.on_property_changed(self, property_name)

    # Методы для работы с валидаторами
    def add_property_changing_listener(self, listener: PropertyChangingListenerProtocol):
        if listener not in self._changing_listeners:
            self._changing_listeners.append(listener)

    def remove_property_changing_listener(self, listener: PropertyChangingListenerProtocol):
        if listener in self._changing_listeners:
            self._changing_listeners.remove(listener)

    def _validate_property_change(self, property_name: str, old_value: T, new_value: T) -> bool:
        for listener in self._changing_listeners:
            if not listener.on_property_changing(self, property_name, old_value, new_value):
                return False
        return True


