from Validators import NameValidator, AgeValidator
from Logger import LoggerListener
from User import User


if __name__ == "__main__":
    user = User("Alice", 5)

    logger = LoggerListener()
    age_validator = AgeValidator()
    name_validator = NameValidator()

    user.add_property_changed_listener(logger)
    user.add_property_changing_listener(age_validator)
    user.add_property_changing_listener(name_validator)

    print("Корректные изменения:")
    user.name = "Felo-de-se"
    user.age = 35

    print("\nНекорректные изменения:")
    user.name = ""
    user.age = -5
    user.age = 150

    print("\nИтоговый класс:")
    print(f"Name: {user.name}, Age: {user.age}")