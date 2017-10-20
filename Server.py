import socket
import sys
import random

def broadcast(grupo, msg):
    for i in grupo:
        i.send(msg.encode('utf-8'))
def cria_baralho():
    # carta, naipe, valor
    baralho = [("4", "ouros", 1), ("4", "espadas", 1), ("4", "copas", 1), ("4", "paus", 1),
                ("5", "ouros", 2), ("5", "espadas", 2), ("5", "copas", 2), ("5", "paus", 2),
                ("6", "ouros", 3), ("6", "espadas", 3), ("6", "copas", 3), ("6", "paus", 3),
                ("7", "ouros", 4), ("7", "espadas", 4), ("7", "copas", 4), ("7", "paus", 4),
                ("8", "ouros", 5), ("8", "espadas", 5), ("8", "copas", 5), ("8", "paus", 5),
                ("9", "ouros", 6), ("9", "espadas", 6), ("9", "copas", 6), ("9", "paus", 6),
                ("10", "ouros", 7), ("10", "espadas", 7), ("10", "copas", 7), ("10", "paus", 7),
                ("dama", "ouros", 8), ("dama", "espadas", 8), ("dama", "copas", 8), ("dama", "paus", 8),
                ("valete", "ouros", 9), ("valete", "espadas", 9), ("valete", "copas", 9), ("valete", "paus", 9),
                ("rei", "ouros", 10), ("rei", "espadas", 10), ("rei", "copas", 10), ("rei", "paus", 10),
                ("as", "ouros", 11), ("as", "espadas", 11), ("as", "copas", 11), ("as", "paus", 11),
                ("2", "ouros", 12), ("2", "espadas", 12), ("2", "copas", 12), ("2", "paus", 12),
                ("3", "ouros", 13), ("3", "espadas", 13), ("3", "copas", 13), ("3", "paus", 13)
    ]
    return baralho
def encode(letra,Nplayer,carta=' '):
    msg = letra+':'+Nplayer+':'+carta
    return msg

def distribui_cartas(grupo, maos, baralho):
    if len(maos)!=0:
        for p in range(0, len(maos)):
            maos.remove()
    cartas = [] # lista vazia de cartas à enviar
    carta=[]
    #precisa pegar 3 cartas por jogador + o vira
    for i in range (0, 7):
        cartas.append(baralho.pop())
    for j in range (0, 2):
        for k in range(0,3):
            carta.append(cartas.pop())
        #transforma as cartas em strings, para serem enviadas
        print(str(len(carta)))
        envio=carta[0][0]+' '+carta[0][1]+' '+carta[1][0]+' '+carta[1][1]+' '+carta[2][0]+' '+carta[2][1]
        grupo[j].send(envio.encode('utf-8'))      
        for f in range (0,3):
            maos.append(carta.pop())
    return cartas.pop()

def mao():
    num=rodada()
    if (num==-1):
        return
    else:
        num=rodada()



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
mao_jogadores=[]
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
        time1.append(addr)
    else:
        time2.append(addr)
    aviso=('voce e o jogador |%d|. aguarde todos os jogadores conectarem'% i)
    jogadores[i-1].send(aviso.encode('utf-8'))
    if i==2:#alterar para jogar com o numero certo de pessoas
        break
msg='\n o jogo iniciara agora.'
broadcast(jogadores,msg)
baralho = cria_baralho()
random.shuffle(baralho)
vira = distribui_cartas(jogadores,mao_jogadores, baralho)
msg='O vira desta mão é %s de %s'%(vira[0],vira[1])
broadcast(jogadores,msg)
#a partir daqui, devem ser pedidas as entradas especificas de cada jogador
inicial=0#jogador que vai começar a mão
atual=0#jogador da vez
esperando=1
while 1:
    mao()
    #msg= ('v:%s'% str(atual+1))
    #jogadores[atual].send(msg.encode('utf-8'))
    #while esperando:
    #    escolha=soquete.recv(1024)
    #   if escolha[1]== addr[atual]:
    #      opcoes=escolha[0].decode('utf-8')
