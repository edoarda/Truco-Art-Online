import socket
import sys

#tentar criar um socket
c_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print ('soquete criado')
#eis aqui a porta de destino
destino=sys.argv[1]
porta=int(sys.argv[2])

print ('tentando acessar a porta '+ str(porta) +' do local '+ destino)
#precisamos esperar os 4 jogadores
c_sock.connect((destino,porta))
print ('conectado ao servidor')
aviso=c_sock.recv(1024)
print (aviso.decode('utf-8'))
msg=c_sock.recv(1024)
print (msg.decode('utf-8'))
msg=c_sock.recv(1024)
print (msg.decode('utf-8'))
msg=c_sock.recv(1024)
print (msg.decode('utf-8'))
