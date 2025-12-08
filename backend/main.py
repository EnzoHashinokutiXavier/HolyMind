from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel
from .auth import router as auth_router
from fastapi.staticfiles import StaticFiles 
from starlette import status
from fastapi.responses import FileResponse, RedirectResponse
from .exibirdb import router as showdb_router  # import what you need
from dotenv import load_dotenv
from .functions import load_user_info
import os
from .auth import verificarToken
from .database.buildDB import create_tables
from contextlib import asynccontextmanager
from openai import OpenAI

# Carrega o arquivo .env
load_dotenv()
# Carrega a variavel do env
api_key = os.getenv("OPENAI_API_KEY")
# Protege contra a falta de chave definida
if not api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable not set.")
# Cria o cliente para usar a API
client = OpenAI(api_key=api_key)

# --- ciclo de vida ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("INFO:    🚀 Inicializando servidor...")
    await create_tables()  # executa na inicialização, criando o banco de dados caso nao tenha
    yield # ISSO DIFERENCIA A INICIALIZAÇÃO DO ENCERRAMENTO DO FASTAPI
    print("INFO:    🛑 Encerrando servidor...")  # executa no shutdown

# --- Instância principal do app ---
app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(showdb_router)

# Modelo base da requisição de texto
class TextRequest(BaseModel):  # Id do usuário e pergunta 
    user_id: int
    text: str

# -Rota-unica------------------------------------------- Desenvolvendo
@app.post("/ai-explanation")
async def ai_explanation(req: TextRequest):
    try:
        data = load_user_info(req.user_id)  # carrega o modelo da ia e o prompt para system
        response = client.chat.completions.create(
            model = data[0],  # data[0] = modelo
            messages = [
                {"role": "system", "content": f"{data[1]}"},  # data[1] = prompt

                {"role": "user", "content": f"{req.text}"}    #req.text = pergunta do usuario
            ]
        )
        ## chat_register() #registrar no historico do usuário ---------- função ainda n existe
        return{"explanation": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------------------------------

# Monta os arquivos da pasta 'static' 
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "static")), name="static")

# Define um GET endpoint na rota de url /
@app.get("/")
async def main_page(request: Request):
    return FileResponse(os.path.join(os.path.dirname(__file__), "..", "static", "index.html"))

@app.get("/auth") 
async def auth_page_verify(request: Request):
    
    try:
        # 1. Tenta verificar o token. Se houver, a linha abaixo executa.
        await verificarToken(request) 
  
        # 2. Se o token for válido, redireciona o usuário para a rota principal (/)
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND) 
        
    except HTTPException:
        # 3. Se verificarToken levantar HTTPException (não logado), exibe a página de login.
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        AUTH_HTML_PATH = os.path.join(BASE_DIR, "..", "static", "auth", "index.html")

        return FileResponse(AUTH_HTML_PATH)
