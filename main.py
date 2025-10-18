import os
import django

# Вказуємо Django, де шукати налаштування
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dance_school.settings')

# Ініціалізація Django
django.setup()

# Тепер можна імпортувати модулі, які використовують ORM
from repositories.RepositoryManager import RepositoryManager

if __name__ == "__main__":
    repo = RepositoryManager()

    print("Всі клієнти:")
    all_clients = repo.clients.get_all()
    print(all_clients)

    print("\nКлієнт з id=1:")
    client = repo.clients.get_by_id(1)
    print(client)
