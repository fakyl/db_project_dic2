#coding:utf-8 
import socket
(host,port) = ('localhost',8888)

try:
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect( (host,port) )
    msg = socket.recv(1024).decode("utf8")
    print(msg) 
    session=True
    requete=input(">>>")   
    while session==True:                      
        if requete=="exit":
            session=False
        else : 
            requete=requete.encode("utf8")                         
            socket.sendall(requete)
            reponse = socket.recv(1024).decode("utf8")  # reception
            print('Reponse: ' + reponse)  # show in terminal
            requete=input(">>>")  

#fin de session
    print("session fermée à bientot!")     
    
except ConnectionRefusedError: 
    print("echec connection")
finally:
    socket.close()
