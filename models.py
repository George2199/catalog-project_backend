from extensions import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    role = db.Column(db.String(20), default="user")
    is_banned = db.Column(db.Boolean, default=False)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    section = db.Column(db.String(100))
    tags = db.Column(db.Text)
    last_updated = db.Column(db.DateTime)
    contact_info = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey("resource.id"), nullable=False)
    image_url = db.Column(db.Text, nullable=False)
