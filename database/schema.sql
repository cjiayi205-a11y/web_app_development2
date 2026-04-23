CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
    is_default INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    record_date TEXT NOT NULL,
    note TEXT,
    category_id INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories (id)
);

CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT NOT NULL UNIQUE,
    amount REAL NOT NULL
);

-- 插入預設分類 (使用 INSERT OR IGNORE 避免重複執行時報錯)
INSERT OR IGNORE INTO categories (id, name, type, is_default) VALUES 
(1, '飲食', 'expense', 1),
(2, '交通', 'expense', 1),
(3, '購物', 'expense', 1),
(4, '娛樂', 'expense', 1),
(5, '薪水', 'income', 1),
(6, '投資', 'income', 1);
