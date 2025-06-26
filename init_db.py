from app import create_app
from app.models import db  # This triggers all model imports & db instance

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully!")
