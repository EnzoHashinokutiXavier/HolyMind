import sqlite3

def create_tables():

    conn = sqlite3.connect("backend/database/holymind.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            age INTEGER NOT NULL,
            denomination TEXT DEFAULT 'no',
            knowledge_level TEXT DEFAULT 'low'
            setup TEXT NOT NULL DEFAULT 'no'
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            response_level TEXT DEFAULT 'simple',
            teachings_example BOOLEAN DEFAULT 0,
            comparison_to_original_writings BOOLEAN DEFAULT 0,
            various_interpretations BOOLEAN DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            question_count INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            date TEXT NOT NULL       
        );
    ''')

    conn.commit()
    conn.close()
    print("INFO:    ✅ Banco de dados inicializado com sucesso.")
