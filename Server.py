import socket
import sys

#tentar criar um socket
soquete=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print ('soquete criado')
#escolhe uma porta do hospedeiro pro bind
hospedeiro=socket.gethostname()#descobre o nome da maquina em que esta rodando
porta=int(sys.argv[1])
soquete.bind((hospedeiro,porta))
print ('soquete colocado na porta '+ str(porta) +' do local '+ hospedeiro)
#precisamos esperar os 4 jogadores
soquete.listen(4)
jogadores = []
#divisão dos jogadores em times
time1 = []
time2= []
i=0

while 1:
    #O servidor fica aguardando as conexoes aqui
    Scliente, addr=soquete.accept()
    print ('o cliente %s parece ter conectado'%str(addr[0]))
    jogadores.append(Scliente)#para mensagens gerais
    i=i+1
    if i%2==1:#separa os jogadores em duplas pra facilitar comunicação
        time1.append(Scliente)
    else:
        time2.append(Scliente)
    aviso=('voce e o jogador %d. aguarde todos os jogadores conectarem'% i)
    jogadores[i-1].send(aviso.encode('ascii'))
    if i==2:#alterar para jogar com o numero certo de pessoas
        break
msg='\n o jogo iniciara agora.'
for i in jogadores:
    i.send(msg.encode('ascii'))
