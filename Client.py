import socket


#tentar criar um socket
c_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print ('soquete criado')
#eis aqui a porta de destino
hospedeiro=socket.gethostname()
porta=4000

print ('tentando acessar a porta'+ str(porta))
#precisamos esperar os 4 jogadores
c_sock.connect((hospedeiro,porta))
print ('conectado ao servidor')
