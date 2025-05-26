from Protocols import T
from Protocols import PropertyChangingListenerProtocol, DataChangingProtocol


class NameValidator(PropertyChangingListenerProtocol):
    def on_property_changing(self, obj: DataChangingProtocol, property_name: str, old_value: T, new_value: T):
        if property_name == "name":
            if not isinstance(new_value, str):
                print("[NameValidator] Имя должно быть строкой")
                return False
            if len(new_value) == 0:
                print("[NameValidator] Имя не может быть пустым")
                return False
            if len(new_value) > 50:
                print("[NameValidator] Имя слишком длинное")
                return False
        return True


class AgeValidator(PropertyChangingListenerProtocol):
    def on_property_changing(self, obj: DataChangingProtocol, property_name: str, old_value: T, new_value: T):
        if property_name == "age":
            if not isinstance(new_value, int):
                print("[AgeValidator] Возраст должен быть цифрой")
                return False
            if new_value < 0:
                print("[AgeValidator] Возраст не может быть отрицательным")
                return False
            if new_value > 120:
                print("[AgeValidator] Возраст выгядит нереалистично")
                return False
        return True


