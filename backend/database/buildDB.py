import aiosqlite

async def create_tables():

    async with aiosqlite.connect("backend/database/holymind.db") as db:
        await db.execute("PRAGMA foreign_keys = ON;")

        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                age INTEGER NOT NULL,
                denomination TEXT DEFAULT 'no',
                knowledge_level TEXT DEFAULT 'low',
                setup TEXT NOT NULL DEFAULT 'no'
            );
        ''')

        await db.execute('''
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

        await db.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                question_count INTEGER NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                date TEXT NOT NULL       
            );
        ''')

        await db.commit()
        print("INFO:    ✅ Banco de dados inicializado com sucesso.")


    
