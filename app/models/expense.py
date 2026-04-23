from .db import get_db_connection

class ExpenseModel:
    @staticmethod
    def get_all(month=None):
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
        conn.close()
        return [dict(e) for e in expenses]

    @staticmethod
    def get_by_id(expense_id):
        conn = get_db_connection()
        query = '''
            SELECT e.*, c.name as category_name, c.type as category_type
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            WHERE e.id = ?
        '''
        expense = conn.execute(query, (expense_id,)).fetchone()
        conn.close()
        return dict(expense) if expense else None

    @staticmethod
    def create(amount, record_date, note, category_id):
        conn = get_db_connection()
        cursor = conn.execute(
            'INSERT INTO expenses (amount, record_date, note, category_id) VALUES (?, ?, ?, ?)',
            (amount, record_date, note, category_id)
        )
        conn.commit()
        expense_id = cursor.lastrowid
        conn.close()
        return expense_id

    @staticmethod
    def update(expense_id, amount, record_date, note, category_id):
        conn = get_db_connection()
        conn.execute(
            'UPDATE expenses SET amount = ?, record_date = ?, note = ?, category_id = ? WHERE id = ?',
            (amount, record_date, note, category_id, expense_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(expense_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        conn.close()
