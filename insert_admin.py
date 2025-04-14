from app import app, db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    try:
        existing_admin = User.query.filter_by(username='admin').first()
        if existing_admin:
            print("⚠ Администратор уже существует")
            print(f"Логин: {existing_admin.username}")
            print(f"❓ Пароль не может быть извлечён (он захеширован). Используй admin123, если ты его задавал.")
        else:
            password = 'admin123'
            admin = User(
                username='admin',
                email='admin@mail.com',
                password_hash=generate_password_hash(password),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Администратор добавлен:")
            print(f"Логин: {admin.username}")
            print(f"Пароль: {password}")
    except Exception as e:
        db.session.rollback()
        print("❌ Ошибка при добавлении администратора:", str(e))
