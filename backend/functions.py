import json
import sqlite3

def register(question, type, answer):
    try:
        conn = sqlite3.connect('backend/history.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            question TEXT NOT NULL,
            type TEXT NOT NULL,
            answer TEXT NOT NULL
        )
        ''')
        cursor.execute("INSERT INTO history (question, type, answer) VALUES (?, ?, ?)", (question, type, answer))
        conn.commit()
    except Exception as e:
        print(f"Erro ao registrar histórico: {e}")  # Log no console do servidor
    finally:
        if 'conn' in locals():
            conn.close()

def check_history():
    try:
        conn = sqlite3.connect('backend/history.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            question TEXT NOT NULL,
            type TEXT NOT NULL,
            answer TEXT NOT NULL
        )
        ''')
        cursor.execute("SELECT * FROM history")
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        history = [dict(zip(columns, row)) for row in rows]
        return history  # Retorna a lista diretamente (FastAPI serializa para JSON)
    except Exception as e:
        print(f"Erro ao verificar histórico: {e}")  # Log no console do servidor
        return []  # Retorna lista vazia em caso de erro
    finally:
        if 'conn' in locals():
            conn.close()

def load_prompts(type):
    data = ''
    with open("backend\\prompts.json", "r", encoding='utf-8') as file:
        prompts = json.load(file)

        data += f"{prompts['identity']}\n"
        data += f"{prompts['limitations']}\n"
        data += f"{prompts['explanation']}\n"
        data += f"{prompts['language']}\n"

        if type == 1:
            data += f"{prompts['general']}\n"
        elif type == 2:
            data += f"{prompts['practical']}\n"
        elif type == 3:
            data += f"{prompts['interpretation']}\n"

        return data