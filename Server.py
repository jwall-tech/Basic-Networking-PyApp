import time
import threading
import logging
import socket

class Connection():
    def __init__(self,server,address,connection):
        self.address = address
        self.ident = "USER "+str(address[0])
        self.connection = connection
        self.server = server
        self.requestCache = {}
        self.connected = True

        def func(data):
            print("from "+str(self.ident)+" data: "+str(data))

            if data.startswith("setuser"):
                self.ident = data[8:]
                msg = "changed username to "+self.ident
                self.connection.send(msg.encode())
            else:
                self.connection.send(data.encode())
            
        self.DataFunc = func
        
        self.addRequestCache(time.time(),"Connection")

        def conLoop():
            while True:
                
                data = self.connection.recv(1024).decode()
            
                if not data:
                    break

                self.DataFunc(data)

        self.conLoopThread = threading.Thread(target=conLoop)
        self.conLoopThread.start()

    def addRequestCache(self,Timestamp,RequestData):
        self.requestCache[str(Timestamp)] = RequestData

    def disconnect(self):
        self.connected = False
        self.connection = None
        self.server.connsInt -= 1

    def newIdent(self,ident):
        self.ident = ident

    def clearCache(self):
        self.requestCache = {}

    def newDataFunc(self,newFunc):
        self.DataFunc = newFunc


class Server():
    def __init__(self,host,port,maxConnections):
        self.host = host
        self.port = port
        self.maxConns = maxConnections
        self.connsInt = 0
        
        self.connections = {}
        
        self.socket = socket.socket()
        self.socket.bind((host,port))
        
        def ListenForConnection():
            self.socket.listen(2)
            conn,addr = self.socket.accept()
            print("conn from: "+str(addr))
            self.newConnection(conn,addr)

        while True:
            if self.connsInt < self.maxConns:
                ListenForConnection()
                

    def newConnection(self,conn,addr):
        self.connsInt =+ 1
        myCon = Connection(self,addr,conn)
        self.connections[str(addr)] = myCon

myServ = Server("192.168.0.17",5000,100)
            
