import random
from datetime import datetime, timedelta
from faker import Faker

from app import app
from models import db, User, Resource

fake = Faker()

# Генерация пользователей
def create_users(n=5):
    users = []
    for i in range(n):
        user = User(
            username=fake.user_name() + str(i),
            email=fake.unique.email(),
            password_hash=fake.sha256(),
        )
        db.session.add(user)
        users.append(user)
    db.session.commit()
    return users

# Генерация ресурсов
def create_resources(users, n=100):
    for i in range(n):
        user = random.choice(users)
        resource = Resource(
            title=fake.sentence(nb_words=6),
            url=fake.url(),
            description=fake.paragraph(nb_sentences=3),
            section=random.choice(["science", "tech", "history", "math", "culture"]),
            tags=", ".join(fake.words(nb=4)),
            last_updated=fake.date_time_between(start_date="-1y", end_date="now"),
            contact_info=fake.email(),
            user_id=user.id
        )
        db.session.add(resource)
    db.session.commit()

# Основной запуск
with app.app_context():
    print("Добавляем пользователей и ресурсы...")
    users = create_users()
    create_resources(users)
    print("Готово: 5 пользователей и 100 ресурсов добавлены в БД.")
