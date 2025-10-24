from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
import sqlite3
from jose import jwt, JWTError
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel
import bcrypt

# ----- Configuração Inicial --------
env_path = "./.env"
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter(prefix="/auth", tags=["auth"])

# ------ Funções auxiliares ------

def get_db_connection():
    conn = sqlite3.connect("backend/database/holymind.db", timeout = 10)
    conn.row_factory = sqlite3.Row
    return conn

def gerarToken(username: str, response: Response):
    payload = {"sub": username, "exp": datetime.now(timezone.utc) + timedelta(hours=1)}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=3600
    )
    return token

def verificarToken(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Não Autenticado")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalido ou expirado!")

# ------- Modelo Pydantic-------

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# ------ ROTAS -----------------

# @router.post("/register")
@router.post("/register") 
def register(user: UserRegister): 
    conn = get_db_connection() 
    cursor = conn.cursor() 

    if len(user.password) < 8: 
        raise HTTPException(status_code=400, detail="Senha deve ter no mínimo 8 caracteres.") 
    
    password_bytes = user.password.encode('utf-8') 
    salt = bcrypt.gensalt() 
    senhahash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    try: 
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, senhahash)) 
        conn.commit() 
        return {"message": f"Usuário {user.username} registrado com sucesso!"}
    except sqlite3.IntegrityError: 
        raise HTTPException(status_code=400, detail="Usuário já existe") 
    
    finally:
        conn.close() 


# @router.post("/login")
@router.post("/login") 
def login(user: UserLogin, response: Response):
    conn = get_db_connection() 
    cursor = conn.cursor() 
    cursor.execute("SELECT password FROM users WHERE username = ?", (user.username,)) 
    row = cursor.fetchone() 

    if row is None: 
        raise HTTPException(status_code=401, detail="Credenciais Invalidas") 
    else: 
        senhaUSER = row["password"] 
     
    #cursor.execute("SELECT username FROM users WHERE email = ?", (user.username,))
    #rowuser = cursor.fetchone()
    #username = rowuser["username"]

    if bcrypt.checkpw(user.password.encode('utf-8'), senhaUSER.encode('utf-8')): 
        token = gerarToken(user.username, response)
        return {"message": "Login foi feito! senha igual", "access_token": token, "token_type": "bearer"}

    else:
        raise HTTPException(status_code=401, detail="Credenciais Invalidas")

# ------------------------------
