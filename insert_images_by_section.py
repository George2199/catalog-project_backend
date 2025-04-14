from app import app, db
from models import Resource, Image

section_to_image = {
    "science": "/static/images/sections/science.jpg",
    "tech": "/static/images/sections/tech.jpg",
    "history": "/static/images/sections/history.jpg",
    "math": "/static/images/sections/math.jpg",
    "culture": "/static/images/sections/culture.jpg",
    "education": "/static/images/sections/education.jpg",
    "misc": "/static/images/sections/misc.jpg",
}

with app.app_context():
    count = 0
    resources = Resource.query.all()
    for res in resources:
        has_image = Image.query.filter_by(resource_id=res.id).first()
        if has_image:
            continue  # Пропускаем, если уже есть хоть одно изображение

        image_path = section_to_image.get(res.section)
        if image_path:
            db.session.add(Image(resource_id=res.id, image_url=image_path))
            count += 1

    db.session.commit()
    print(f"✓ Добавлено {count} изображений (по одному на ресурс).")
