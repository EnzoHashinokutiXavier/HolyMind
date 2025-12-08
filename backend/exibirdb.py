from fastapi import HTTPException
import aiosqlite
from .database.database import get_db
from fastapi import APIRouter, Depends
from .auth import admin_required

router = APIRouter(prefix="/admin", tags=["showdb"])

@router.get('/showdb')
async def show_users_with_preferences(user: dict = Depends(admin_required), db: aiosqlite.Connection = Depends(get_db)):
    try:

        cursor = await db.execute('''
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

        rows = await cursor.fetchall()

        if rows:
            print("\n--- Usuários e Preferências ---")
            users_data = []
        
            for row in rows:
                users_info = {
                    "id": row[0],
                    "username": row[1],
                    "age": row[2],
                    "denomination": row[3],
                    "knowledge_level": row[4],
                    "preferences": {
                        "response_level": row[5],
                        "teachings_example": bool(row[6]),
                        "comparison_to_original_writings": bool(row[7]),
                        "various_interpretations": bool(row[8])
                    }
                }
                users_data.append(users_info)

                print(f"""
ID: {row[0]} | Nome: {row[1]} | Idade: {row[2]} | Denominação: {row[3]} | Conhecimento: {row[4]}
  ↳ Resposta: {row[5]} | Exemplos: {bool(row[6])} | Comparação: {bool(row[7])} | Várias Interpretações: {bool(row[8])}
                """)

            return {"usuarios": users_data}
        else:
            print("Nenhum usuário registrado ainda.")
            return {"mensagem": "Nenhum usuário registrado ainda."}

    except Exception as e:
        print(f"Erro ao exibir usuários: {e}")
        raise HTTPException(status_code=500, detail="Erro inteiro ao acessar o banco de dados")

