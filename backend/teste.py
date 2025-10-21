import sqlite3

def register_user(username, password, age):
    try:
        conn = sqlite3.connect('backend/database/holymind.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            age INTEGER NOT NULL,
            denomination TEXT DEFAULT 'no',
            knowledge_level TEXT DEFAULT 'low'
        );
                       
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
        #inserir usuário
        cursor.execute('''INSERT INTO users (username, password, age) 
                       VALUES (?, ?, ?)
                       ''', (username, password, age))
        
        #pegar id
        user_id = cursor.lastrowid
        #inserir
        cursor.execute('''
        INSERT INTO preferences(user_id)
        VALUES (?)     
        ''', (user_id,))

        conn.commit()
    except Exception as e:
        print(f"Erro ao registrar usuário: {e}")  # Log no console do servidor
    finally:
        if 'conn' in locals():
            conn.close()

register_user('Enzo', '123', 18)

