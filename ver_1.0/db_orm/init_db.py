from .base import BaseMikrotik, BaseUsers, engine_mikrotik, engine_users

def init_db():
    """Создание всех таблиц"""
    BaseMikrotik.metadata.create_all(engine_mikrotik)
    BaseUsers.metadata.create_all(engine_users)

if __name__ == "__main__":
    init_db()