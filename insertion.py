import json
import os
from sql_parsing import insert_query_parse
base = "base.json"
table = "Student"
def insertion(base,table,enregistrement ):
    with open(base) as json_data:
        data_dict = json.load(json_data)
        liste=[]
        liste=data_dict.copy()
        liste[1].append(enregistrement)
        data_dict=json.dumps(liste,indent=4)
        fichier = open(base,'w')
        fichier.write(data_dict)
        fichier.close()
def insert(query):
    res = insert_query_parse(query)
    #print("tableName: ", res.tableName)
    #print("valuesList: ", res.valuesList)
    val = (res.valuesList).asList()
    values = val[1]
    print(values)
    keys=['id','name','surname','adress','hobbies', 'numberPhone']
    enregistrement = {}
    for key, value in zip(keys,values):
        if "'" in str(value): value = value[1:-1]
        enregistrement.update({key:value})
    #print(enregistrement)
    #print(values)
    insertion(base,table,enregistrement)