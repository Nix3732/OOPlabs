from rep import UserRepository
from User import User
from auth import AuthService


if __name__ == "__main__":
    user_repo = UserRepository()
    auth_service = AuthService(user_repo)

    users = [
        User(0, "manager", "admin2025", "Alice Johnson", "alice.johnson@example.com"),
        User(1, "visitor", "guestpass", "Egor", "bob.carter@example.com", "42 Oak Street")
    ]

    for user in users:
        if not user_repo.get_by_id(user.id):
            user_repo.add(user)

    print("1. Попытка автоматического входа:")
    print(f"Авторизован:    {auth_service.is_authorized}")
    print(f"Текущий пользователь: {auth_service.current_user}")
    print()

    print("2. Попытка входа с неправильным паролем:")
    print(f"Успех:          {auth_service.sign_in('visitor', 'notright')}")
    print(f"Авторизован:    {auth_service.is_authorized}")
    print(f"Текущий пользователь: {auth_service.current_user}")
    print()

    print("3. Успешный вход:")
    print(f"Успех:          {auth_service.sign_in('manager', 'admin2025')}")
    print(f"Авторизован:    {auth_service.is_authorized}")
    print(f"Текущий пользователь: {auth_service.current_user}")
    print()

    print("4. Выход из системы:")
    auth_service.sign_out()
    print(f"Авторизован:    {auth_service.is_authorized}")
    print(f"Текущий пользователь: {auth_service.current_user}")
    print()

    print("5. Вход другим пользователем после выхода:")
    print(f"Успех:          {auth_service.sign_in('visitor', 'guestpass')}")
    print(f"Авторизован:    {auth_service.is_authorized}")
    print(f"Текущий пользователь: {auth_service.current_user}")
    print()

    print("6. Обновление данных пользователя:")
    user = user_repo.get_by_login("visitor")
    user.name = "Vitya"
    user_repo.update(user)
    print("Обновленные данные пользователя:")
    print(user_repo.get_by_id(user.id))
