import sqlite3

def show_users_with_preferences():
    try:
        conn = sqlite3.connect('backend/database/holymind.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT 
            u.id, 
            u.username, 
            u.age, 
            u.denomination, 
            u.knowledge_level,
            p.response_level,
            p.teachings_example,
            p.comparison_to_original_writings,
            p.various_interpretations
        FROM users u
        LEFT JOIN preferences p ON u.id = p.user_id
        ''')

        rows = cursor.fetchall()

        if rows:
            print("\n--- Usuários e Preferências ---")
            for row in rows:
                print(f"""
ID: {row[0]} | Nome: {row[1]} | Idade: {row[2]} | Denominação: {row[3]} | Conhecimento: {row[4]}
  ↳ Resposta: {row[5]} | Exemplos: {bool(row[6])} | Comparação: {bool(row[7])} | Várias Interpretações: {bool(row[8])}
                """)
        else:
            print("Nenhum usuário registrado ainda.")

    except Exception as e:
        print(f"Erro ao exibir usuários: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

# Teste
show_users_with_preferences()
