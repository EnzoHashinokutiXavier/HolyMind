import aiosqlite    
from contextlib import asynccontextmanager


@asynccontextmanager
async def get_db_connection(): # Inicializador do banco de dados
    conn = None
    try:
        # Tenta conectar-se ao banco de dados SQLite. 
        conn = await aiosqlite.connect("backend/database/holymind.db")

        # Configura a fábrica de linhas (row_factory) para aiosqlite.Row.
        # Isso permite que os resultados das consultas sejam acessados como 
        # objetos que se comportam como dicionários (acesso por nome da coluna), 
        # em vez de simples tuplas.
        conn.row_factory = aiosqlite.Row

        # 'yield' é o ponto onde o bloco 'with' começa. 
        # O objeto 'conn' é retornado para o 'as' do bloco 'with'.
        yield conn
    finally:
        # O bloco 'finally' garante que o código dentro dele será executado 
        # mesmo se ocorrer uma exceção (erro) ou se o bloco 'with' for concluído.
        if conn:
            # Fecha a conexão com o banco de dados de forma assíncrona.
            await conn.close()