import socket
import sys
import random
from collections import deque

class jogo:

    #var gerais
    jogadores=[]
    mao_jogadores=[]
    cartas_jogadas=[]
    inicial=0
    atual = 0
    time1=[]
    time2=[]
    mao=[]
    vira = []
    resposta = ['x','x']
    baralho = []
    #var truco
    ult_truco=-1
    pontuacao=0

    def __init__(self,jogadores,mao,cartas_jogadas=[]):
        self.inicial=0
        self.atual=0
        self.cartas_jogadas=cartas_jogadas

    def divide_times(self):
        if(jogadores.length == 4):
            self.time1.append(jogadores[0])
            self.time1.append(jogadores[1])
            self.time2.append(jogadores[2])
            self.time2.append(jogadores[3])
        else:
            print('faltam jogadores')

    def retornaPontuacao(self,):
        print('pensar depois')
        return self.pontuacao

    def retornaTime(self,numero):
        for i in self.time1:
            if numero==time1[i]:
                return 1
            elif numero==time2[i]:
                return 2
        return 0

    def resp_truco(self,tipo):
        #compara a resposta recebida
        if self.resposta =='x':
            #se nao houver anterior, salva e retorna 'x' indicando pra esperar segunda resposta
            self.resposta = tipo
            return 'x'
        elif self.resposta == 'R':
            #Retruco so e valido se ambos retornarem retruco
            if tipo=='R':
                self.resposta='x'
                return tipo
            else:
                temp = self.resposta
                self.resposta='x'
                return temp
        else:
            #se outro jogador ja tiver respondido antes
            if self.resposta == tipo:
                #se forem iguais, zera e retorna
                self.resposta='x'
                return tipo
            else:
                #se forem diferentes retorna a que ja estava e zera a variavel
                temp = self.resposta
                self.resposta='x'
                return temp

    def timeOposto(self,nmjogador):
        if nmjogador%2==0:
            return 1
        else:
            return 2

    def timeJogador(self,nmjogador):
        if nmjogador%2==0:
            return 2
        else:
            return 1

    def proxJogador(self):
        self.atual=self.atual+1
        if self.atual>4:
            atual=0#super gambiarra


def broadcast(grupo, msg):
    broad = encode('M',0,msg)
    for i in grupo:
        i.send(broad.encode('utf-8'))

#parte de comparação
def compara(carta1, carta2, carta3, carta4, vira):
    valor=[carta1[2],carta2[2],carta3[2],carta4[2]]
    naipe=[carta1[1],carta2[1],carta3[1],carta4[1]]
    naipeValor = []
    for i in range(0 , 4):
        if valor[i] == vira[2]+1:
            valor[i]=14
    maior = max(valor)
    comMaiorNumero = valor.count(maior)
    if comMaiorNumero == 1:
        indexMaior = 0
        for i in range(0,4):
            if valor[i] == maior:
                indexMaior = i
        return indexMaior
    if comMaiorNumero > 1:
        indexMaior = []
        for i in range(0,4):
            if valor[i] == maior:
                indexMaior.append(i)
            if naipe[i] != "ouros" and naipe[i] != "espadas" and naipe[i] != "copas" and naipe[i] != "paus":
                #se chegou aqui entao todas as cartas foram jogadas viradas pra baixo
                naipeValor.append(0)
            if naipe[i] == "ouros":
                naipeValor.append(1)
            if naipe[i] == "espadas":
                naipeValor.append(2)
            if naipe[i] == "copas":
                naipeValor.append(3)
            if naipe[i] == "paus":
                naipeValor.append(4)
        indexM = 0
        if max(naipeValor) == 0:
            return -1
        for i in range(len(indexMaior)):
            print(naipeValor[indexMaior[i]])
            if naipeValor[indexMaior[i]]>indexM:
                indexM = indexMaior[i]
        return indexM

#fim parte de comparação de cartas

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

#parte de codificação e decodificação de mensagens
def encode(letra,Nplayer,opt=' '):
    msg = letra+':'+Nplayer+':'+opt + '@Ç'
    return msg

# função que vai recebendo coisas, separa bonitinho no caso do python ter sido um amorzinho e peidado nas mensagens e taca o que sobrou numa fila
#msgs terminam com @Ç
def receber(soquete, fila):
    msg = ""
    if len(fila) != 0:
        try:
            msg = fila.pop()
            if '@' in msg: # msg tem fim. yay!
                msg = msg.split('@')
                return msg[0]
        # se fila.pop() soltar IndexError, é pq não tem uma msg completa na fila e é pra ouvir mensagens
        except IndexError:
            fila.append(msg)
            msg = ""
            #sair de tudo e ir pro while dali de baixo

    #caso não tenha uma mensagem terminada na fila
    while 1:
        #é pra dar listen no sockete aqui
        #msg += "poneifeliz@Çbatat@ÇcacetepululuanteçAAAAA"
        msg += soquete.recv(1024).decode('utf-8')
        if 'Ç' in msg:
            msg = msg.split('Ç')
            # dá append na fila a todas as mensagens com o @ no final pra gente saber que aquilo é uma msg inteira
            for i in range (1, len(msg)):
                fila.append(msg[i])
            # tira o @ da msg[0] e retorna
            msg = msg[0].split('@')
            return msg[0]



def decodeSvr(codigo,jogo):
    numJogador=jogo.atual
    guarda=codigo.split(':',3)
    if guarda[1]==numJogador:
        if guarda[0]== 'F':
            msg=('o jogador %s jogou uma carta fechada'% str(guarda[1]+1))
            envio=encode('M','4',msg)
            broadcast(jogadores,envio)
            jogar_carta(guarda[2],guarda[1],1,C_jogadas,jogo.mao)
        elif guarda[0] == 'A':
            jogar_carta(guarda[2],guarda[1],0,C_jogadas,jogo.mao)
            msg=('o jogador %s jogou %s de %s'%(str(guarda[1]+1),C_jogadas[guarda[1]][0],C_jogadas[guarda[1]][1]))
            envio=encode('M',4,msg)
            broadcast(jogadores,envio)
        elif guarda[0] == 'T':
            if jogo.pontuacao>12 or jogo.ult_truco == guarda[1]:
                notifica = encode('X',numJogador)
                jogadores[numJogador] = notifica.encode('utf-8')
            else:
                ult_truco = guarda[1]
                envio=encode(guarda[0],guarda[1])
                if (guarda[1]%2==1):
                    broadcast(time2,envio)
                else:
                    broadcast(time1,envio)
    else:
        if guarda[0]== 'K' or guarda[0]== 'D' or guarda[0]== 'R':
            respt = jogo.resposta('K')
            if respt == 'K':
                mensagem_aceita = encode('M',4,'Truco do time '+jogo.timeOposto(numJogador)+' aceito')
                broadcast(jogo.jogadores,mensagem_aceita)
            elif respt == 'D':
                mensagem_aceita = encode('M',4,'Time '+jogo.timeJogador(numJogador)+' fugiu')
                broadcast(jogo.jogadores,mensagem_aceita)
            elif respt== 'R':
                #if jogo.ult_truco == jogo.retornaTime(numJogador):
                mensagem_aceita = encode('T',numJogador,'Time '+jogo.timeJogador(numJogador)+' pediu Retruco')
                #gambiarra
                if jogo.timeJogador(numJogador) == 1:
                    broadcast(jogo.time2,mensagem_aceita)
                else:
                    broadcast(jogo.time1,mensagem_aceita)
            else:
                mensagem_aceita = encode('M',4,'Aguardando resposta dos oponentes')
                broadcast(jogo.jogadores,mensagem_aceita)
        else:
            #enviar mensagem pro jogador da vez que veio errado e dar a vez de novo
            print('falta')







    #elif guarda[2] in ['r','a','f']:#fugir
    #    if guarda[2]=='f':
            #arrumar um meio de declarar derrota da dupla que fugiu
            #e começar uma nova mão
   #     elif guarda[2]=='r'and (valor_rodada<=12):#retrucar
            #
            #


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
        envio='C'+':'+ carta[0][0]+':'+carta[0][1]+':'+carta[1][0]+':'+carta[1][1]+':'+carta[2][0]+':'+carta[2][1]
        grupo[j].send(envio.encode('utf-8'))
        for f in range (0,3):
            maos.append(carta.pop())
    return cartas.pop()

#def mao():
#    num=rodada()
#    if (num==-1):
#        return
#    else:
#        num=rodada()

def jogar_carta(carta,player,tipo,lista,maos):
    if tipo:
        #joga uma carta fechada
        lista[player]=('coringa','nada',0)
    else:
        lista[player]=maos[(player*3)+carta]

#tentar criar um socket

#fila de mensagens
fila = deque()
soquete=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print ('soquete criado')
#escolhe uma porta do hospedeiro pro bind
hospedeiro=socket.gethostname()#descobre o nome da maquina em que esta rodando
porta=int(sys.argv[1])
soquete.bind((hospedeiro,porta))
print ('soquete colocado na porta '+ str(porta) +' do local '+ hospedeiro)
#precisamos esperar os 4 jogadores
soquete.listen(4)
newGame = jogo()
jogadores = []
mao_jogadores=[]
C_jogadas=[(),(),(),()]
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
    jogo.jogadores.append(addr)
    if i%2==1:#separa os jogadores em duplas pra facilitar comunicação
        jogo.time1.append(addr)
    else:
        jogo.time2.append(addr)
    #aviso=('voce e o jogador :%d:. aguarde todos os jogadores conectarem'% i)
    aviso=encode('N',i," ")
    jogo.jogadores[i-1].send(aviso.encode('utf-8'))
    if i==2:#alterar para jogar com o numero certo de pessoas
        break
msg='\n o jogo iniciara agora.'
broadcast(jogo.jogadores,msg)
jogo.baralho = cria_baralho()
jogo.baralho=random.shuffle(jogo.baralho)
vira = distribui_cartas(jogadores,mao_jogadores, jogo.baralho)
jogo.vira=[vira[0],vira[1]]
msg='O vira desta mão é %s de %s'%(vira[0],vira[1])
#jogadores[0].send(msg.encode('utf-8'))
#jogadores[1].send(msg.encode('utf-8'))
#jogadores[0].send(encode('M',0,msg))
broadcast(jogo.jogadores,msg)

#a partir daqui, devem ser pedidas as entradas especificas de cada jogador

while 1:
    #ta estranho mas não vou mudar o de baixo
    broadcast(jogadores,encode('V',str(jogo.atual)))

    recebido=jogadores[jogo.atual].recv(1024)
    decodeSvr(recebido.decode('utf-8'),jogo)
    jogo.proxJogador()

    #msg= ('V:%s: '% str(atual))
    #jogadores[atual].send(msg.encode('utf-8'))
    #while esperando:
    #    escolha=soquete.recv(1024)
    #   if escolha[1]== addr[atual]:
    #      opcoes=escolha[0].decode('utf-8')
