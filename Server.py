import socket


#tentar criar um socket
soquete=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print ('soquete criado')
#escolhe uma porta do hospedeiro pro bind
hospedeiro=socket.gethostname()
porta=4001
soquete.bind((hospedeiro,porta))
print ('soquete colocado na porta '+ str(porta))
#precisamos esperar os 4 jogadores
soquete.listen(4)
jogadores = []
i=0

while 1:
    Scliente, addr=soquete.accept()
    print ('o cliente %s parece ter conectado'%str(addr[0]))
    jogadores.append(Scliente)
    i=i+1
    aviso=('voce e o jogador %d. aguarde todos os jogadores conectarem'% i)
    jogadores[i-1].send(aviso.encode('ascii'))
    if i==2:
        break
msg='o jogo iniciara agora.'
for i in jogadores:
    i.send(msg.encode('ascii'))
