import json
import sqlite3

def register(question, type, answer):
    conn = sqlite3.connect('backend/history.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS history (
        question TEXT NOT NULL,
        type TEXT NOT NULL,
        answer TEXT NOT NULL
    )
    ''')
    cursor.execute("INSERT INTO history (question, type, answer) VALUES (?, ?, ?)",(question, type, answer))
    conn.commit()
    conn.close()


def check_history():
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
    column = [description[0] for description in cursor.description]
    history = [dict(zip(column, row)) for row in rows]
    conn.close()
    return json.dumps(history, indent=4, ensure_ascii=False)


def load_prompts(type):
    data = ''
    with open("backend\\prompts.json", "r", encoding='utf-8') as file:
        prompts = json.load(file)  # <-- Aqui está a correção

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
