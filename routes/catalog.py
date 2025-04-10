from flask import Blueprint, jsonify, request
from models import Resource

catalog_bp = Blueprint('catalog', __name__)

@catalog_bp.route('/api/resources')
def get_resources():
    # Параметры запроса
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)
    sections = request.args.getlist('section')  # <- массив всех section=...

    query = Resource.query

    # Если выбраны конкретные разделы
    if sections:
        query = query.filter(Resource.section.in_(sections))

    # Пагинация
    resources = query.offset(offset).limit(limit).all()

    # Ответ
    return jsonify([
        {
            "id": r.id,
            "title": r.title,
            "url": r.url,
            "description": r.description,
            "section": r.section,
            "tags": r.tags,
            "last_updated": r.last_updated.strftime('%Y-%m-%d'),
            "contact_info": r.contact_info
        }
        for r in resources
    ])
