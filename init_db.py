from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    admin = User.query.filter_by(email='admin@example.com').first()
    if admin:
        admin.is_admin = True
        db.session.commit()
        print("Admin promu.")