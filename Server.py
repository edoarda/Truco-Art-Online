import socket


#tentar criar um socket
soquete=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print ('soquete criado')
#escolhe uma porta do hospedeiro pro bind
hospedeiro=socket.gethostname()
porta=4000
soquete.bind((hospedeiro,porta))
print ('soquete colocado na porta '+ str(porta))
#precisamos esperar os 4 jogadores
soquete.listen(4)

while True:
    Scliente=soquete.accept()
    print ('o cliente '+str(Scliente)+' parece ter conectado')
