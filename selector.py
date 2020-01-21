import json
import os
from sql_parsing import select_parsing
base = "base.json"
def selectionAll(base,table):
    with open(base) as json_data:
        data_dict = json.load(json_data)
        json_data.close()
        print(json.dumps(data_dict[table], indent=4))
        return data_dict[table]

def selection(base,table,colonne,option):
    with open(base) as json_data:
        data_dict = json.load(json_data)
        json_data.close()
        for i in range(len(data_dict[table])):
            val=data_dict[table][i][colonne]
            if val==option:
                print(json.dumps({colonne:data_dict[table][i][colonne]}, indent=4))
                return data_dict[table][i]
        if not val==option:
            print("not found")

def select(query):
    result = select_parsing(query)
    condpart = query[query.index('select') + len('select'):query.index('from')]
    if 'where' not in query: tablepart = query[query.index('from') + len('from') + 1:]
    else: tablepart = query[query.index('from') + len('from') + 1:query.index('where') -1]
    colonne = condpart[1:-1]
    wherepart = query[query.index('where') + len('where') + 1:]
    option = wherepart.split('=')[1]
    if "'" not in option:
        try:
            option = int(option)
        except Exception as e:
            print(e)
    else: option=option[1:-1]

    if condpart == '*':
        selectionAll(base,tablepart)
    else:
        selection(base,tablepart,colonne,option)
