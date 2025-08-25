from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import FileResponse   
from pydantic import BaseModel
from csv import DictReader, DictWriter
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
@app.post("/general-explanation")
async def general_explanation(req: TextRequest):
    try:
        # Chama a API da OpenAI para responder a conversa
        response = client.chat.completions.create(
            model = "gpt-4o-mini", # Modelo do chat
            messages=[
                # Define padrão de comportamento do sistema
                {"role": "system", "content": "You are a theologian with a large biblical understanding who answers clearly, in a simple way, passages and books of the Bible"},

                # Define o pedido do usuario
                {"role": "user", "content" : f"Explain to me the following passage from the Bible: {req.text} If I said something that is not part of the Bible, do not respond to what I said and let me know."}
            ]
        )
        register(req.text, "general_explanation", response.choices[0].message.content)
        # Retorna a explicação do assistente em JSON
        return{"explanation": response.choices[0].message.content}
    except Exception as e:
        # Se algo der errado, retorna um erro HTTP 500 com os detalhes
        raise HTTPException(status_code=500, detail=str(e))
    
    #Endpoint para uso futuro
@app.post("/practical-explanation")
async def practical_explanation(req: TextRequest):
    try:
        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a theologian with a deep biblical understanding. Your explanations reflect what message God wanted to convey in a passage or book, showing how to apply the teachings in everyday life."},

                {"role": "user", "content": f"Explain to me the following passage from the Bible: {req.text} If I said something that is not part of the Bible, do not respond to what I said and let me know."}
            ]
        )
        register(req.text, "pratical_explanation", response.choices[0].message.content)
        return{"explanation": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    #Endpoint para uso futuro
@app.post("/interpretations-explanation")
async def interpretations_explanation(req: TextRequest):
    try:
        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a theologian with extensive religious knowledge, who explains biblical passages showing their interpretations according to each Christian religion."},

                {"role": "user", "content": f"Explain to me the following passage from the Bible: {req.text} If I said something that is not part of the Bible, do not respond to what I said and let me know."}
            ]
        )
        register(req.text, "interpretations_explanation", response.choices[0].message.content)
        return{"explanation": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history-view")
async def hitory_view():
    response = ''
    with open("history.csv", newline='', encoding='utf-8') as historyfile:
        reader = DictReader(historyfile)
        for row in reader:
            response += f"Question : {row['question']}\n"
            response += f"Type : {row['type']}\n"
            response += f"Answer : {row['answer']}\n"
            response += '-' * 40 + "\n"
        return response


# Monta os arquivos da pasta 'static' 
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "static")), name="static")


# Define um GET endpoint na rota de url /
@app.get("/")
async def root():
    # Retorna o arquivo html
    return FileResponse(os.path.join(os.path.dirname(__file__), "..", "static", "index.html"))


def register(question, type, answer):
    if not question:
        print("Pergunta vazia, registro ignorado.")
        return
    with open("backend\\history.csv", mode='a', encoding='utf-8', newline='') as arquivo:  
        escrever = DictWriter(arquivo, fieldnames=["question", "type", "answer"])
        if arquivo.tell() == 0:
            escrever.writeheader()
        escrever.writerow({"question": question, "type": type, "answer": answer})