cursor.execute("SELECT * FROM history")
    rows = cursor.fetchall()

    # Pega os nomes das colunas
    colunas = [description[0] for description in cursor.description]

    # Transforma em lista de dicionários
    historico = [dict(zip(colunas, row)) for row in rows]

    conn.close()

    # Retorna como JSON (ou pode printar se preferir)
    return json.dumps(historico, indent=4, ensure_ascii=False)