from functions import check_history, register

register("pergunta1", "tipo1", "resposta1")

json = check_history()
print(json)