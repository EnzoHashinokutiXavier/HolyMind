from csv import DictReader

response = ''
with open("history.csv", newline='', encoding='utf-8') as historyfile:
    reader = DictReader(historyfile)
    for row in reader:
        response += f"Question : {row['question']}\n"
        response += f"Type : {row['type']}\n"
        response += f"Answer : {row['answer']}\n"
        response += '-' * 60 + "\n"
    print(response)