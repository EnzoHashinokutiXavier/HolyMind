from functions import check_history, register

register("pergunta3", "tipo3", "resposta3")

json = check_history()
print(json)