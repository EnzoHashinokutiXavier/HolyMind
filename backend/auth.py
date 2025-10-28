from datetime import datetime, timedelta, timezone, date
import os
import sqlite3
from jose import jwt, JWTError
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, Request, Response, status
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
        max_age=3600,
        path="/"
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
    
def calcularIdade(data_str: str) -> int:
    try:
        data_nascimento = datetime.strptime(data_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=400, 
            detail="Formato de data inválido. Use AAAA-MM-DD."
        )

    hoje = date.today()
    
    idade = hoje.year - data_nascimento.year
    if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
        idade -= 1

    return idade


# ------- Modelo Pydantic-------

class UserRegister(BaseModel):
    username: str
    password: str
    birthDate: str
    

class UserLogin(BaseModel):
    username: str
    password: str

# ------ ROTAS -----------------

@router.post("/register") 
def register(user: UserRegister): 
    conn = get_db_connection() 
    cursor = conn.cursor() 

    age = calcularIdade(user.birthDate)

    if (age < 12):
        raise HTTPException(status_code=400, detail=f"Usuario {user.username} não tem idade minima para se cadastrar")
    
    if len(user.password) < 8: 
        raise HTTPException(status_code=400, detail="Senha deve ter no mínimo 8 caracteres.") 
    
    password_bytes = user.password.encode('utf-8') 
    salt = bcrypt.gensalt() 
    senhahash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    try: 
        cursor.execute("INSERT INTO users (username, password, age) VALUES (?, ?, ?)", ( user.username, senhahash, age)) 
        user_id = cursor.lastrowid
        conn.commit()

        cursor.execute("INSERT INTO preferences(user_id) VALUES (?)", (user_id,))
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
     
    #cursor.execute("SELECT username FROM users WHERE email = ?", (user.email,))
    #rowuser = cursor.fetchone()
    #username = rowuser["username"]

    if bcrypt.checkpw(user.password.encode('utf-8'), senhaUSER.encode('utf-8')):
        token = gerarToken(user.username, response)
        return {"message": "Login realizado com sucesso"}

    else:
        raise HTTPException(status_code=401, detail="Credenciais Invalidas")


@router.get("/status")
def get_login_status(request: Request):
    try:
        verificarToken(request) # Tenta verificar o token no cookie (HttpOnly)
        return {"logado": True}
    except HTTPException:
        return {"logado": False}
    

@router.post("/logout")
def logout():
    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Logout realizado com sucesso!"}
    )
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=False,
        samesite="lax",
        path="/"
    )
    return response
