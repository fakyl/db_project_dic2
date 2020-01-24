import json
import os
from sql_parsing import create_table_query_parse

def creerTable(table,colonne):
	liste = []
	for x in range(len(colonne)):
		print(colonne[x])
		liste.append(colonne[x])
	dic = {}
	for a in range(len(liste)):
		for b in range(2):
			if b % 2 == 0:
				column = str(liste[a][b])
				dic[column] = 'Null'
	x = 0
	with open('base.json') as f:
		json_data  = json.load(f)
		liste=[]  
		for key, value in json_data:
			tupl = (key, value)
			liste.append(tupl)
	tupl = (table, dic)
	liste.append(tupl)
	json_data = json.dumps(liste, indent=4)
	fichier = open('base.json','w')
	fichier.write(json_data)
	fichier.close()
	#print(data)
def creeTable(query):
	res = create_table_query_parse(query)
	print("table", res.tableName)
	print("column", res.columnList)
	colonne = res.columnList
	table = res.tableName
	creerTable(table,colonne)