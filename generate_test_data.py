import os
import django
import random
from faker import Faker

# Устанавливаем Django окружение
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from main.models import (
    CustomUser, Manufacturers, Tobaccos, TasteCategories, Mixes, MixLikes, MixFavorites, MixTobacco
)

fake = Faker()

# Количество записей для генерации
NUM_USERS = 10
NUM_MANUFACTURERS = 5
NUM_TOBACCOS = 20
NUM_CATEGORIES = 5
NUM_MIXES = 10


def create_users():
    """Создаёт тестовых пользователей."""
    users = []
    for _ in range(NUM_USERS):
        user = CustomUser.objects.create_user(
            email=fake.unique.email(),
            username=fake.unique.user_name(),
            password="password123",
        )
        users.append(user)
    print(f"Создано {len(users)} пользователей.")
    return users


def create_manufacturers():
    """Создаёт производителей."""
    manufacturers = []
    for _ in range(NUM_MANUFACTURERS):
        manufacturer = Manufacturers.objects.create(
            name=fake.company(),
            description=fake.text(max_nb_chars=200),
            image=None,  # Можно указать путь к тестовому изображению
        )
        manufacturers.append(manufacturer)
    print(f"Создано {len(manufacturers)} производителей.")
    return manufacturers


def create_tobaccos(manufacturers):
    """Создаёт табаки."""
    tobaccos = []
    for _ in range(NUM_TOBACCOS):
        tobacco = Tobaccos.objects.create(
            manufacturer=random.choice(manufacturers),
            taste=fake.word(),
            image=None,  # Можно указать путь к тестовому изображению
            tobacco_strength=random.choice([str(i) for i in range(11)]),
            tobacco_resistance=random.choice(['low', 'middle', 'high']),
            tobacco_smokiness=random.choice(['low', 'middle', 'high']),
            description=fake.text(max_nb_chars=200),
        )
        tobaccos.append(tobacco)
    print(f"Создано {len(tobaccos)} табаков.")
    return tobaccos


def create_categories():
    """Создаёт категории вкусов."""
    categories = []
    for _ in range(NUM_CATEGORIES):
        category = TasteCategories.objects.create(
            name=fake.word().capitalize()
        )
        categories.append(category)
    print(f"Создано {len(categories)} категорий вкусов.")
    return categories


def create_mixes(users, categories, tobaccos):
    """Создаёт миксы."""
    mixes = []
    for _ in range(NUM_MIXES):
        mix = Mixes.objects.create(
            name=fake.word().capitalize(),
            description=fake.text(max_nb_chars=300),
            banner=None,  # Можно указать путь к тестовому изображению
            tasteType=random.choice(['fruit', 'gastro', 'sweet', 'grass', 'fresh']),
            author=random.choice(users),
        )
        # Добавляем категории
        mix.categories.add(*random.sample(categories, k=random.randint(1, len(categories))))

        # Добавляем табаки
        num_tobaccos_in_mix = random.randint(1, 5)
        for _ in range(num_tobaccos_in_mix):
            MixTobacco.objects.create(
                mix=mix,
                tobacco=random.choice(tobaccos),
                weight=random.randint(10, 50),
            )
        mixes.append(mix)
    print(f"Создано {len(mixes)} миксов.")
    return mixes


def create_likes_and_favorites(users, mixes):
    """Создаёт лайки и избранное для миксов."""
    likes = []
    favorites = []
    for mix in mixes:
        # Лайки
        num_likes = random.randint(1, len(users))
        for user in random.sample(users, k=num_likes):
            likes.append(MixLikes.objects.create(mix=mix, user=user))

        # Избранное
        num_favorites = random.randint(1, len(users))
        for user in random.sample(users, k=num_favorites):
            favorites.append(MixFavorites.objects.create(mix=mix, user=user))

    print(f"Создано {len(likes)} лайков и {len(favorites)} избранных миксов.")


def generate_test_data():
    """Генерация всех тестовых данных."""
    print("Начинаем генерацию тестовых данных...")
    users = create_users()
    manufacturers = create_manufacturers()
    tobaccos = create_tobaccos(manufacturers)
    categories = create_categories()
    mixes = create_mixes(users, categories, tobaccos)
    create_likes_and_favorites(users, mixes)
    print("Генерация тестовых данных завершена.")


if __name__ == "__main__":
    generate_test_data()