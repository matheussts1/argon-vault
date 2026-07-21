import os

database_path = os.getenv('DATABASE_URL')

def connection_to_url(db):
    if db:
        if db.startswith("postgres://"):
            db = db.replace("postgres://", "postgresql://", 1)

        return db

def local_db_connection():
    bdbase = os.path.abspath(os.path.dirname(__file__))
    instance_path = os.path.join(bdbase, 'instance')

    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
    
    return 'sqlite:///' + os.path.join(instance_path, 'user.db')