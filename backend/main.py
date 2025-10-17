from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from .functions import load_prompts, check_history, register, load_user_info
import os
from openai import OpenAI

# Carrega a variavel do env
api_key = os.getenv("OPENAI_API_KEY")
# Protege contra a falta de chave definida
if not api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable not set.")
# Cria o cliente para usar a API
client = OpenAI(api_key=api_key)

app = FastAPI()


# Modelo base da requisição de texto
class TextRequest(BaseModel):
    user_id: int
    text: str


# -Rota-unica------------------------------------------- Desenvolvendo
@app.post("/ai-explanation")
async def ai_explanation(req: TextRequest):
    try:
        data = load_user_info(req.user_id)
        response = client.chat.completions.create(
            model = data[0],
            messages = [
                {"role": "system", "content": f"{data[1]}"},

                {"role": "user", "content": f"{req.text}"}
            ]
        )
        register()#registrar no historico do usuário
        return{"explanation": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------------------------------


@app.get("/history-view")
async def history_view():
    response = check_history()
    return response


# Monta os arquivos da pasta 'static' 
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "static")), name="static")


# Define um GET endpoint na rota de url /
@app.get("/")
async def root():
    # Retorna o arquivo html
    return FileResponse(os.path.join(os.path.dirname(__file__), "..", "static", "index.html"))


