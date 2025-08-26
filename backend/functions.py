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
    with open("prompts.json", "r") as file:
        data += file['identity']
        data += file['limitations']
        data += file['explanations']
        if type == 1:
            data += file['general']
        elif type == 2:
            data += file['practical']
        elif type == 3:
            data += file["interpretation"]
        return data