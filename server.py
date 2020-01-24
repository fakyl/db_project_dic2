#coding:utf-8 
import socket
import threading
import creerBD
import creerTable
import insertion
import selector
import supprimer
def Client(conn,ip,port):
    msg="Bien connecté"
    msg=msg.encode("utf8")
    conn.send(msg) 
    
    while True:
        requete = conn.recv(1024).decode("utf8")
        if not requete:
            print("connection du client fermée")
            conn.close()
            break
        print("requete de l'utilisateur: " + str(requete)) #just for debug
        req = requete.split(" ")
        if(req[0] == "create"):
            if(req[1] == "database"):
                creerBD.creerBD(requete)
            if(req[1] == 'table'):
                creerTable.creeTable(requete)
        if(req[0] == "insert"):
            insertion.insert(requete)
        if(req[0] == "select"):
            selector.select(requete)
        # if(req[0] == "delete"):
        #     supprimer.delete(requete)
        reponse="Bien passé"
        conn.send(reponse.encode("utf8"))  # send data to the client

#main
(host,port) = ('',8888)
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind( (host,port) )
print("Serveur demarré")
while True:
    socket.listen(10)
    (conn,address)=socket.accept()
    ip, port = str(address[0]), str(address[1])    
    print("nouveau client")
    threading.Thread(target=Client,args=(conn, ip, port) ).start()


#fin de session
conn.close()
socket.close()
