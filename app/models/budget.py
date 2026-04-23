from .db import get_db_connection

class BudgetModel:
    @staticmethod
    def get_by_month(month):
        conn = get_db_connection()
        budget = conn.execute('SELECT * FROM budgets WHERE month = ?', (month,)).fetchone()
        conn.close()
        return dict(budget) if budget else None

    @staticmethod
    def set_budget(month, amount):
        conn = get_db_connection()
        existing = conn.execute('SELECT id FROM budgets WHERE month = ?', (month,)).fetchone()
        if existing:
            conn.execute('UPDATE budgets SET amount = ? WHERE month = ?', (amount, month))
        else:
            conn.execute('INSERT INTO budgets (month, amount) VALUES (?, ?)', (month, amount))
        conn.commit()
        conn.close()
