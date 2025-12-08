from datetime import datetime, timedelta, timezone, date
import os
import aiosqlite # type: ignore
from jose import jwt, JWTError  # type: ignore
from dotenv import load_dotenv # type: ignore
from fastapi.responses import JSONResponse
from starlette import status
from fastapi import APIRouter, HTTPException, Request, Response, status, Depends
from pydantic import BaseModel
from fastapi.responses import FileResponse, RedirectResponse
from .database.database import get_db
import bcrypt # type: ignore

# ----- Configuração Inicial --------
env_path = "./.env"
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter(prefix="/auth", tags=["auth"])
AUTH_HTML_PATH = os.path.join(os.path.dirname(__file__), "static", "auth", "index.html")

# ------ Funções auxiliares ------

async def gerarToken(username: str, response: Response):

    if (username == "admin"):
        role = "admin"
    else:
        role = "user"

    payload = {"sub": username, "role": role,"exp": datetime.now(timezone.utc) + timedelta(hours=1)}
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

async def verificarToken(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Não Autenticado")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalido ou expirado!")
    
async def calcularIdade(data_str: str) -> int:
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

def admin_required(user: dict = Depends(verificarToken)):
        if user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Acesso restrito a administradores")
        return user


# ------- Modelo Pydantic-------

class UserRegister(BaseModel):
    username: str
    password: str
    birthDate: str
    

class UserLogin(BaseModel):
    username: str
    password: str

class SetupResponse(BaseModel):
    denominationValue: str
    levelValue: str
    modeSetup: int
    

# ------ ROTAS -----------------

@router.post("/register")
async def register(user: UserRegister, db: aiosqlite.Connection = Depends(get_db)): 

    age = await calcularIdade(user.birthDate)

    if (age < 12):
        raise HTTPException(status_code=400, detail=f"Usuario {user.username} não tem idade minima para se cadastrar")
    
    if len(user.password) < 8: 
        raise HTTPException(status_code=400, detail="Senha deve ter no mínimo 8 caracteres.") 
    
    password_bytes = user.password.encode('utf-8') 
    salt = bcrypt.gensalt() 
    senhahash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    try: 
        cursor = await db.execute("INSERT INTO users (username, password, age) VALUES (?, ?, ?)", ( user.username, senhahash, age)) 
        user_id = cursor.lastrowid
        await db.commit()

        await db.execute("INSERT INTO preferences(user_id) VALUES (?)", (user_id,))
        await db.commit()
        return {"message": f"Usuário {user.username} registrado com sucesso!"}
    except aiosqlite.IntegrityError:
        raise HTTPException(status_code=400, detail="Usuário já existe")

# @router.post("/login")
@router.post("/login") 
async def login(user: UserLogin, response: Response, db: aiosqlite.Connection = Depends(get_db)):
    try:
        
        cursor = await db.execute("SELECT password FROM users WHERE username = ?", (user.username,)) 
        row = await cursor.fetchone()

        if row is None: 
            raise HTTPException(status_code=401, detail="Credenciais Invalidas") 
        else: 
            senhaUSER = row["password"] 
     
    #cursor.execute("SELECT username FROM users WHERE email = ?", (user.email,))
    #rowuser = cursor.fetchone()
    #username = rowuser["username"]

        if bcrypt.checkpw(user.password.encode('utf-8'), senhaUSER.encode('utf-8')):
            token = await gerarToken(user.username, response)
            return {"message": "Login realizado com sucesso"}

    except:
        raise HTTPException(status_code=401, detail="Credenciais Invalidas")


@router.get("/status")
async def get_login_status(request: Request, db: aiosqlite.Connection = Depends(get_db)):
    try:
        payload = await verificarToken(request) # Tenta verificar o token no cookie (HttpOnly)
        username = payload.get("sub")


        cursor = await db.execute("SELECT setup FROM users WHERE username = ?", (username,))
        row = await cursor.fetchone()

        setup_status = row[0] if row else "no"

        return {
            "logado": True,
            "setup": setup_status
        }
    except HTTPException:
        return {
            "logado": False,
            "setup": "no"
        }
    

@router.post("/logout")
async def logout():
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

@router.post("/save-setup")
async def saveSetup(userdata: SetupResponse, request: Request, db: aiosqlite.Connection = Depends(get_db)):
  
    try:
        payload = await verificarToken(request)

        username = payload.get('sub')
        
        modoSetup = None 
        
        if userdata.modeSetup == 0 and userdata.denominationValue == 'none' and userdata.levelValue == 'none':
            modoSetup = 'skip'
        elif userdata.modeSetup == 1:
            modoSetup = 'yes'
        
        if modoSetup is None: 
            raise HTTPException(status_code=400, detail="Entrada Inválida para o tipo de configuração.")

        
        if modoSetup == 'skip':
            await db.execute("UPDATE users SET setup = ? WHERE username = ?", (modoSetup, username))
        
        elif modoSetup == 'yes':
            await db.execute("UPDATE users SET setup = ?, denomination = ?, knowledge_level = ? WHERE username = ?", (modoSetup, userdata.denominationValue, userdata.levelValue, username))

        await db.commit()
        
    except HTTPException as e:
        raise e
        
    except Exception as e:
        await db.rollback() 
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
    
    return {"message": "Configuração salva com sucesso!", "mode": modoSetup}


