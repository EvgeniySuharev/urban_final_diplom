from backend.database import SessionLocal


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""Функция выполняет подключение к БД, а затем независимо
 от результата подключения закрывает его"""