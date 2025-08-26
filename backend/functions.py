import json
from csv import DictWriter

def register(question, type, answer):
    if not question:
        print("Pergunta vazia, registro ignorado.")
        return
    with open("backend\\history.csv", mode='a', encoding='utf-8', newline='') as file:  
        write = DictWriter(file, fieldnames=["question", "type", "answer"])
        if file.tell() == 0:
            write.writeheader()
        write.writerow({"question": question, "type": type, "answer": answer})


def load_prompts(type):
    data = ''
    with open("backend\\prompts.json", "r", encoding='utf-8') as file:
        prompts = json.load(file)  # <-- Aqui está a correção

        data += f"{prompts['identity']}\n"
        data += f"{prompts['limitations']}\n"
        data += f"{prompts['explanation']}\n"

        if type == 1:
            data += f"{prompts['general']}\n"
        elif type == 2:
            data += f"{prompts['practical']}\n"
        elif type == 3:
            data += f"{prompts['interpretation']}\n"

        return data
