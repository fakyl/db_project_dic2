import json
import os
from sql_parsing import create_db_parse

def creerBaseDeDonnee(bd):
    fichier=open( bd + ".json" ,"w")
    fichier.write("Hello")
    fichier.close()
def creerBD(query):
	resul = create_db_parse(query)
	#print("ident: ", resul.dbName)
	bd=str(resul.dbName[0])
	creerBaseDeDonnee(bd)
	