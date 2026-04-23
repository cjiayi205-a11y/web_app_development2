from .db import get_db_connection
import sqlite3

class CategoryModel:
    """分類資料模型，負責處理 categories 表的 CRUD 操作。"""

    @staticmethod
    def get_all():
        """
        取得所有分類。
        :return: 包含所有分類字典的列表，若發生錯誤則回傳空列表。
        """
        try:
            conn = get_db_connection()
            categories = conn.execute('SELECT * FROM categories ORDER BY type, id').fetchall()
            return [dict(c) for c in categories]
        except sqlite3.Error as e:
            print(f"Database error in CategoryModel.get_all: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_id(category_id):
        """
        根據 ID 取得單筆分類。
        :param category_id: 分類 ID
        :return: 分類字典，若找不到或發生錯誤則回傳 None。
        """
        try:
            conn = get_db_connection()
            category = conn.execute('SELECT * FROM categories WHERE id = ?', (category_id,)).fetchone()
            return dict(category) if category else None
        except sqlite3.Error as e:
            print(f"Database error in CategoryModel.get_by_id: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def create(name, type):
        """
        新增一筆自訂分類。
        :param name: 分類名稱
        :param type: 分類類型 ('income' 或 'expense')
        :return: 新增的分類 ID，若發生錯誤則回傳 None。
        """
        try:
            conn = get_db_connection()
            cursor = conn.execute('INSERT INTO categories (name, type, is_default) VALUES (?, ?, 0)', (name, type))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in CategoryModel.create: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update(category_id, name, type):
        """
        更新自訂分類（不允許修改預設分類）。
        :param category_id: 分類 ID
        :param name: 新分類名稱
        :param type: 新分類類型
        :return: 成功回傳 True，失敗回傳 False。
        """
        try:
            conn = get_db_connection()
            conn.execute('UPDATE categories SET name = ?, type = ? WHERE id = ? AND is_default = 0', (name, type, category_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in CategoryModel.update: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete(category_id):
        """
        刪除自訂分類（不允許刪除預設分類）。
        :param category_id: 分類 ID
        :return: 成功回傳 True，失敗回傳 False。
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM categories WHERE id = ? AND is_default = 0', (category_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in CategoryModel.delete: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
