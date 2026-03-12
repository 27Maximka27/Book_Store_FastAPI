import psycopg2
from src.configurations.settings import settings

def test_connection():
    try:
        # Подключение к PostgreSQL
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database="postgres",  # Подключаемся к системной БД
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        print("✅ Подключение к PostgreSQL успешно!")
        
        # Проверяем наличие базы данных book_store
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'book_store'")
        exists = cur.fetchone()
        
        if exists:
            print(" База данных 'book_store' существует")
        else:
            print(" База данных 'book_store' не существует")
            cur.execute("CREATE DATABASE book_store")
            print(" База данных 'book_store' создана")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f" Ошибка подключения: {e}")

if __name__ == "__main__":
    test_connection()