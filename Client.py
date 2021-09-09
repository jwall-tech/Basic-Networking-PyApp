import socket
import threading
import logging
import time

class Client():
        def __init__(self,host,port):
                self.host = host
                self.port = port
                self.socket = socket.socket()
                self.socket.connect((host,port))

                def requestLoop():
                        while True:
                                data = self.socket.recv(1024).decode()
                    
                                if not data:
                                    break

                                self.handleRequest(data)
                        
                self.requestLoop = threading.Thread(target=requestLoop)
                self.requestLoop.start()
                
                while True:
                        myInput = input("--> ")
                        self.handleInput(myInput)
                        
        def handleInput(self,uInput):
                self.socket.send(uInput.encode())

                #returnVal = self.socket.recv(1024).decode()

               # if returnVal:
                       # print("Return from server: "+returnVal)
                        

        def handleRequest(self,data):
                print(data)

myClient = Client("IP","PORT")    
