from datetime import datetime, timedelta, timezone, date
import os
import sqlite3
from jose import jwt, JWTError
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, Request, Response, status
from pydantic import BaseModel
import bcrypt

from auth import get_db_connection

def chat_register(user_id, question_count, question, answer, question_date):
    conn = get_db_connection() 
    cursor = conn.cursor() 

    try: 
        cursor.execute("INSERT INTO history(user_id, question_count, question, answer, date) VALUES (?)"
                       , (user_id, question_count, question, answer, question_date))
        conn.commit()
        return {"message": f"Pergunta registrada com sucesso!"}
    except sqlite3.IntegrityError: 
        raise HTTPException(status_code=400, detail="Erro") 
    
    finally:
        conn.close() 


