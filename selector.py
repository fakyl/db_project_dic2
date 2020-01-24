import json
import os
from sql_parsing import select_parsing
base = "base.json"
def selectionAll(base,table):
    with open(base) as json_data:
        data_dict = json.load(json_data)
        #json_data.close()
        print(json.dumps(data_dict[0], indent=4))

def selection(base,table,colonne,option):
    with open(base) as json_data:
        data_dict = json.load(json_data)
        json_data.close()
        for i in range(len(data_dict[0])):
            val=data_dict[0][i][colonne]
            if val==option:
                print(json.dumps({colonne:data_dict[0][i][colonne]}, indent=4))
                return data_dict[0][i]
        if not val==option:
            print("not found")

def select(query):
    result = select_parsing(query)
    #print(result)
    #condpart = result[result.index('select') + len('select'):result.index('from')]
    condpart = result[0] + result[2]
    #if 'where' not in result: tablepart = result[result.index('from') + len('from') + 1:]
    tablepart = result[3]
    #else: tablepart = result[result.index('from') + len('from') + 1:result.index('where') -1]
    colonne = condpart[1:-1]
    #wherepart = result[4]
    #wherepart = result[result[.index('where')] + len('where') + 1:]
    #option = wherepart.split('=')[1]  
    """    
    if "'" not in option:
        try:
            option = int(option)
        except Exception as e:
            print(e)
    else: option=option[1:-1]
    """
    
    print(selectionAll(base,tablepart))
   
