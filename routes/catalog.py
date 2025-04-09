from flask import Blueprint, jsonify
from models import Resource

catalog_bp = Blueprint('catalog', __name__)

@catalog_bp.route('/api/resources')
def get_resources():
    resources = Resource.query.all()
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
