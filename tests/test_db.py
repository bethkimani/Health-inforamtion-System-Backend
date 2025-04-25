from app import create_app, db

app = create_app()
with app.app_context():
    try:
        db.create_all()
        print("Database connected and tables created successfully!")
        print("Tables:", db.engine.table_names())
    except Exception as e:
        print(f"Error: {e}")