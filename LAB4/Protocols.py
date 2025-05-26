from typing import Protocol, TypeVar

T = TypeVar('T')


class PropertyChangedListenerProtocol(Protocol):
    def on_property_changed(self, obj: T, property_name: str):
        ...


class DataChangedProtocol(Protocol):
    def add_property_changed_listener(self, listener: PropertyChangedListenerProtocol):
        ...

    def remove_property_changed_listener(self, listener: PropertyChangedListenerProtocol):
        ...


class PropertyChangingListenerProtocol(Protocol):
    def on_property_changing(self, obj: T, property_name: str, old_value: T, new_value: T) -> bool:
        ...


class DataChangingProtocol(Protocol):
    def add_property_changing_listener(self, listener: PropertyChangingListenerProtocol):
        ...

    def remove_property_changing_listener(self, listener: PropertyChangingListenerProtocol):
        ...
