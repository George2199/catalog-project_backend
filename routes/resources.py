from flask import Blueprint, request, jsonify
from extensions import db
from models import Resource, Image

resource_bp = Blueprint('resources', __name__)

@resource_bp.route("/", methods=["GET"])
def get_all_resources():
    resources = Resource.query.all()
    result = []
    for r in resources:
        result.append({
            "id": r.id,
            "title": r.title,
            "url": r.url,
            "description": r.description,
            "section": r.section,
            "tags": r.tags,
            "last_updated": r.last_updated,
            "contact_info": r.contact_info,
            "user_id": r.user_id
        })
    return jsonify(result)

@resource_bp.route("/", methods=["POST"])
def add_resource():
    data = request.json
    r = Resource(
        title=data["title"],
        url=data["url"],
        description=data.get("description"),
        section=data.get("section"),
        tags=data.get("tags"),
        last_updated=data.get("last_updated"),
        contact_info=data.get("contact_info"),
        user_id=data["user_id"]
    )
    db.session.add(r)
    db.session.commit()
    return jsonify({"message": "Ресурс добавлен", "id": r.id}), 201
