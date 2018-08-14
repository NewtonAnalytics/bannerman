import sqlalchemy

def connect_to_db():
    engine = sqlalchemy.create_engine(
        'sqlite:///' + r'C:\Users\Tyler Hughes\Documents\Kingsmen Repositories\bannerman\bannerman\bannerman.db'
    )
    return engine.connect()