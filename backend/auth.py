from datetime import datetime, timedelta
import os
from pathlib import Path
import sqlite3
from time import timezone
from jose import jwt, JWTError
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel
import bcrypt

# ----- Configuração Inicial --------
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter(prefix="/auth", tags=["auth"])

# ------ Funções auxiliares ------

def get_connection_db():
    conn = sqlite3.connect("", timeout = 10)
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

# @router.post("/login")

# ------------------------------
