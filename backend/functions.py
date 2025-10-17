import json
import sqlite3

def register(question, type, answer):    ##### REFAZER
    try:
        conn = sqlite3.connect('backend/database/history.db')
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

def check_history():   ######## REFAZER
    try:
        conn = sqlite3.connect('backend/database/history.db')
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


def load_prompts(user_info):
    data = ''
    with open("backend\\prompts.json", "r", encoding='utf-8') as file:
        prompts = json.load(file)
        data += f"{prompts['identity']}\n{prompts['limitations']}\n{prompts['explanation']}\n{prompts['language']}\n{prompts['exception']}\n"
        data += "You need to respond to the user based on their information and preferences:"
        data += ""
        # nivel de conhecimento (superficial, mediano, profundo), idade, denominação
        # nivel de resposta (simple, deep), resposta com exemplos de aplicações dos ensinamentos (true, false)
        # comparação com textos originais - hebraico, aramaico, grego (true, false)
        # exibir interpretações de diversas denominações (true, false)
    return data
    

def load_user_info(user_id):
    #abrir database
    #acessar usuário
    #recolher : tipo de resposta

    response_type = x #tipo de resposta

    if response_type == 'simple':
        model = "gpt-4o-mini"
    elif response_type == 'deep':
        model = "gpt-4-turbo"
    else:
        model = "gpt-4o-mini"

    info = x #informações

    prompt = load_prompts(info)

    data = [model, prompt]
    return data