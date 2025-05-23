from src.app import app, db

def init_database():
    with app.app_context():
        # Crea todas las tablas
        db.create_all()
        print("Base de datos inicializada correctamente.")

if __name__ == "__main__":
    init_database()
