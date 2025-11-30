import json
import sqlite3

# ----------------------------------------------------- Desenvolvendo
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

        #inserir usuário
        cursor.execute('''
        INSERT INTO users (username, password, age) 
        VALUES (?, ?, ?)
        ''', (username, password, age))
        
        #pegar id do usuário recém criado
        user_id = cursor.lastrowid

        #inserir preferencias padrão
        cursor.execute('''
        INSERT INTO preferences(user_id)
        VALUES (?)     
        ''', (user_id,))

        # Confirmar as operações
        conn.commit()

        print(f"Usuário '{username}' registrado com sucesso (ID: {user_id})")
        
    except Exception as e:
        print(f"Erro ao registrar usuário: {e}")  # Log no console do servidor
    finally:
        if 'conn' in locals():
            conn.close()

# -----------------------------------------------------

# -------------chat register por usuario---------------------------------------- Desenvolvendo





# -----------------------------------------------------


# Seleciona modelo da ia e carrega prompt
def load_user_info(user_id):
    #abrir database
    conn = sqlite3.connect('backend/database/holymind.db')
    cursor = conn.cursor()
    #acessar usuário
    cursor.execute('SELECT * FROM users WHERE id = ? ', (user_id))
    usuario = cursor.fetchall() #armazena informações do usuário
    #acessar preferencia
    cursor.execute('SELECT * FROM preferences WHERE id = ? ', (user_id))
    preferencia = cursor.fetchall() #armazena informações do usuário

    # carregar prompt
    prompt = ''
    with open("backend\\prompts.json", "r", encoding='utf-8') as file:
        # ler prompts gerais pre definidos
        preset_prompts = json.load(file)
        prompt += f"{preset_prompts['identity']}\n{preset_prompts['limitations']}\n{preset_prompts['explanation']}\n{preset_prompts['language']}\n{preset_prompts['exception']}\n"
        # se usuario deu informações de preferencia, personalizar prompt
        if usuario[0][6] == "yes":
            # adaptar resposta de acordo com o perfil do usuario
            prompt += "You must respond to the user in a manner appropriate to their information ("
            prompt += f"User knowledge level : {usuario[0][5]},  Age : {usuario[0][3]}, Religious denomination : {usuario[0][4]}). \n"
            # seleção de profundidade de resposta
            prompt += f"You must respond in {preferencia[0][2]}"
            # mostrar aplicação pratica dos ensinamentos 
            if preferencia[0][3] == True:
                prompt += " and show how to apply the teachings in practice. \n"
            else:
                prompt += " and you don't need to show how to apply the teachings in practice. \n"
            # mostrar comparação com os textos originais da biblia
            if preferencia[0][4] == True:
                prompt += "Your explanation should include a comparison with the original texts of the Bible (Greek, Hebrew, or Aramaic).\n"
            else:
                prompt += "Your explanation should not include comparisons with the original texts of the Bible (Greek, Hebrew, or Aramaic).\n"
            # mostrar interpretação de diversas denominações
            if preferencia[0][5] == True:
                prompt += "You should explain the point of view of various denominations regarding the topic discussed.\n"
            else:
                prompt += "You shouldn't explain the point of view of various denominations regarding the topic discussed.\n"

    # Definir modelo de ia
    response_type = preferencia[0][2] #tipo de resposta
    if response_type == 'simple':
        model = "gpt-4o-mini"
    elif response_type == 'deep':
        model = "gpt-4-turbo"
    else:
        model = "gpt-4o-mini"

    data = [model, prompt]

    return data