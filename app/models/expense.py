from .db import get_db_connection
import sqlite3

class ExpenseModel:
    """收支紀錄模型，負責處理 expenses 表的 CRUD 操作。"""

    @staticmethod
    def get_all(month=None):
        """
        取得所有收支紀錄，可依月份篩選。
        :param month: 篩選月份，格式 'YYYY-MM'
        :return: 收支紀錄字典的列表。
        """
        try:
            conn = get_db_connection()
            query = '''
                SELECT e.*, c.name as category_name, c.type as category_type
                FROM expenses e
                JOIN categories c ON e.category_id = c.id
            '''
            params = []
            if month:
                query += " WHERE e.record_date LIKE ?"
                params.append(f"{month}-%")
                
            query += " ORDER BY e.record_date DESC, e.id DESC"
            
            expenses = conn.execute(query, tuple(params)).fetchall()
            return [dict(e) for e in expenses]
        except sqlite3.Error as e:
            print(f"Database error in ExpenseModel.get_all: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_id(expense_id):
        """
        根據 ID 取得單筆收支紀錄。
        :param expense_id: 收支紀錄 ID
        :return: 收支紀錄字典，找不到則回傳 None。
        """
        try:
            conn = get_db_connection()
            query = '''
                SELECT e.*, c.name as category_name, c.type as category_type
                FROM expenses e
                JOIN categories c ON e.category_id = c.id
                WHERE e.id = ?
            '''
            expense = conn.execute(query, (expense_id,)).fetchone()
            return dict(expense) if expense else None
        except sqlite3.Error as e:
            print(f"Database error in ExpenseModel.get_by_id: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def create(amount, record_date, note, category_id):
        """
        新增一筆收支紀錄。
        :param amount: 金額
        :param record_date: 日期 (YYYY-MM-DD)
        :param note: 備註
        :param category_id: 分類 ID
        :return: 新增的紀錄 ID，失敗則回傳 None。
        """
        try:
            conn = get_db_connection()
            cursor = conn.execute(
                'INSERT INTO expenses (amount, record_date, note, category_id) VALUES (?, ?, ?, ?)',
                (amount, record_date, note, category_id)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in ExpenseModel.create: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update(expense_id, amount, record_date, note, category_id):
        """
        更新特定的收支紀錄。
        :param expense_id: 紀錄 ID
        :param amount: 新金額
        :param record_date: 新日期
        :param note: 新備註
        :param category_id: 新分類 ID
        :return: 成功回傳 True，失敗回傳 False。
        """
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE expenses SET amount = ?, record_date = ?, note = ?, category_id = ? WHERE id = ?',
                (amount, record_date, note, category_id, expense_id)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in ExpenseModel.update: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete(expense_id):
        """
        刪除特定的收支紀錄。
        :param expense_id: 紀錄 ID
        :return: 成功回傳 True，失敗回傳 False。
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in ExpenseModel.delete: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
