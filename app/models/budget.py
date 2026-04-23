from .db import get_db_connection
import sqlite3

class BudgetModel:
    """預算資料模型，負責處理 budgets 表的操作。"""

    @staticmethod
    def get_by_month(month):
        """
        取得特定月份的預算設定。
        :param month: 月份，格式 'YYYY-MM'
        :return: 預算字典，若無設定則回傳 None。
        """
        try:
            conn = get_db_connection()
            budget = conn.execute('SELECT * FROM budgets WHERE month = ?', (month,)).fetchone()
            return dict(budget) if budget else None
        except sqlite3.Error as e:
            print(f"Database error in BudgetModel.get_by_month: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def set_budget(month, amount):
        """
        設定或更新特定月份的預算（Upsert）。
        :param month: 月份，格式 'YYYY-MM'
        :param amount: 預算金額
        :return: 成功回傳 True，失敗回傳 False。
        """
        try:
            conn = get_db_connection()
            existing = conn.execute('SELECT id FROM budgets WHERE month = ?', (month,)).fetchone()
            if existing:
                conn.execute('UPDATE budgets SET amount = ? WHERE month = ?', (amount, month))
            else:
                conn.execute('INSERT INTO budgets (month, amount) VALUES (?, ?)', (month, amount))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in BudgetModel.set_budget: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
