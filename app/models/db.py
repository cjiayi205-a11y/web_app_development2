import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """
    取得資料庫連線，並設定 row_factory 讓查詢結果能以字典方式存取。
    :return: sqlite3.Connection 物件
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    初始化資料庫，讀取並執行 schema.sql 建表語法與初始資料。
    """
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    try:
        conn = get_db_connection()
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        print("Database initialized successfully.")
    except sqlite3.Error as e:
        print(f"Database error during initialization: {e}")
    except FileNotFoundError:
        print(f"Schema file not found at {schema_path}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
