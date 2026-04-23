from .db import get_db_connection

class CategoryModel:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        categories = conn.execute('SELECT * FROM categories ORDER BY type, id').fetchall()
        conn.close()
        return [dict(c) for c in categories]

    @staticmethod
    def get_by_id(category_id):
        conn = get_db_connection()
        category = conn.execute('SELECT * FROM categories WHERE id = ?', (category_id,)).fetchone()
        conn.close()
        return dict(category) if category else None

    @staticmethod
    def create(name, type):
        conn = get_db_connection()
        cursor = conn.execute('INSERT INTO categories (name, type, is_default) VALUES (?, ?, 0)', (name, type))
        conn.commit()
        category_id = cursor.lastrowid
        conn.close()
        return category_id

    @staticmethod
    def update(category_id, name, type):
        conn = get_db_connection()
        # 只允許修改非預設分類
        conn.execute('UPDATE categories SET name = ?, type = ? WHERE id = ? AND is_default = 0', (name, type, category_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(category_id):
        conn = get_db_connection()
        # 預設分類不允許刪除
        conn.execute('DELETE FROM categories WHERE id = ? AND is_default = 0', (category_id,))
        conn.commit()
        conn.close()
