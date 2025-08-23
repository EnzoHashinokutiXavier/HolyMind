from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import FileResponse   
from pydantic import BaseModel
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
    text: str

# Define um POST endpoint em /aichat
@app.post("/aichat")
async def ai_chat(req: TextRequest):
    try:
        # Chama a API da OpenAI para responder a conversa
        response = client.chat.completions.create(
            model = "gpt-4o-mini", # Modelo do chat
            messages=[
                # Define padrão de comportamento do sistema
                {"role": "system", "content": "You are an assistant that helps the understanding of biblical passages"},

                # Define o pedido do usuario
                {"role": "user", "content" : f"If I ask a question, answer me, if I type a passage, explain it : {req.text}"}
            ]
        )
        # Retorna a explicação do assistente em JSON
        return{"explanation": response.choices[0].message.content}
    except Exception as e:
        # Se algo der errado, retorna um erro HTTP 500 com os detalhes
        raise HTTPException(status_code=500, detail=str(e))
    
    #Endpoint para uso futuro
@app.post("/rotavazia")
async def rota_vazia(req: TextRequest):
    try:
        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages=[
                {"role": "system", "content": ""},

                {"role": "user", "content": ""}
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    #Endpoint para uso futuro
@app.post("/vazio")
async def vazio(req: TextRequest):
    try:
        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages=[
                {"role": "system", "content": ""},

                {"role": "user", "content": ""}
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Monta os arquivos da pasta 'static' 
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "static")), name="static")


# Define um GET endpoint na rota de url /
@app.get("/")
async def root():
    # Retorna o arquivo html
    return FileResponse(os.path.join(os.path.dirname(__file__), "..", "static", "index.html"))
