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

    def __init__(self,C_jogadas=[(),(),("4", "espadas", 1),("5", "copas", 2)]):
        self.inicial=0
        self.atual=0
        self.Cartas_jogadas=C_jogadas

    def divide_times(self):
        if(self.jogadores.length == 4):
            self.time1.append(self.jogadores[0])
            self.time1.append(self.jogadores[1])
            self.time2.append(self.jogadores[2])
            self.time2.append(self.jogadores[3])
        else:
            print('faltam jogadores')

    def retornaPontuacao(self,):
        print('pensar depois')
        return self.pontuacao

    def retornaTime(self,numero):
        for i in self.time1:
            if numero==self.time1[i]:
                return 1
            elif numero==self.time2[i]:
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
    broad = encode('M','0',msg)
    for i in grupo:
        i.sendall(broad.encode('utf-8'))

def manda_um(dest,code,player,opt=' '):
    text=encode(code,player,opt)
    dest.sendall(text.encode('utf-8'))

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
def encode(letra,Nplayer,opt='lixo'):
    msg = letra+':'+Nplayer+':'+opt +'@Ç'
    return msg

# função que vai recebendo coisas, separa bonitinho no caso do python ter sido um amorzinho e peidado nas mensagens e taca o que sobrou numa fila
# função que vai recebendo coisas, separa bonitinho no caso do python ter sido um amorzinho e peidado nas mensagens e taca o que sobrou numa fila
 #msgs terminam com @Ç
#msgs terminam com @Ç
def receber(soquete, fila):
     msg = ""
     if len(fila) != 0:
         try:
             msg = fila.pop()
             if '@' in msg: # msg tem fim. yay!
                 msg = msg.split('@')
                 print(fila)
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
             print(msg)
             print(fila)
             return msg[0]

def decodeSvr(codigo,jogo):
    numJogador=jogo.atual
    guarda=codigo.split(':')
    if guarda[1]==str(numJogador):
        if guarda[0]== 'F':
            msg=('o jogador %s jogou uma carta fechada'% str(guarda[1]))
            broadcast(jogo.jogadores,msg)
            jogar_carta(guarda[2],guarda[1],1,jogo.Cartas_jogadas,jogo.mao)
        elif guarda[0] == 'A':
            jogar_carta(guarda[2],guarda[1],0,jogo.Cartas_jogadas,jogo.mao_jogadores)
            msg=('o jogador %s jogou %s de %s'%(str(guarda[1]),str(jogo.Cartas_jogadas[int(guarda[1])][0]),str(jogo.Cartas_jogadas[int(guarda[1])][1])))
            broadcast(jogo.jogadores,msg)
        elif guarda[0] == 'T':
            if jogo.pontuacao>12 or jogo.ult_truco == guarda[1]:
                notifica = encode('X',numJogador)
                jogo.jogadores[numJogador] = notifica.encode('utf-8')
            else:
                ult_truco = guarda[1]
                envio=encode(guarda[0],guarda[1])
                if (guarda[1]%2==1):
                    broadcast(jogo.time2,envio)
                else:
                    broadcast(jogo.time1,envio)
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
        envio=encode('W',str(j),carta[0][0]+':'+carta[0][1]+':'+carta[1][0]+':'+carta[1][1]+':'+carta[2][0]+':'+carta[2][1])
        print(envio)
        print(sys.getsizeof(envio))
        env=grupo[j].sendall(envio.encode('utf-8'))
        print(env)
        for f in range (0,3):
            maos.append(carta.pop(0))
    print(maos)
    return [maos, cartas.pop()]


def jogar_carta(carta,player,tipo,lista,maos):
    if tipo:
        #joga uma carta fechada
        lista[int(player)]=('coringa','nada',0)
    else:
        print(player)
        lista[int(player)]=maos[(int(player)*3)+int(carta)]

#tentar criar um socket

#fila de mensagens

fila =[]
gamestate=0
soquete=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print ('soquete criado')
#escolhe uma porta do hospedeiro pro bind
hospedeiro=socket.gethostname()#descobre o nome da maquina em que esta rodando
porta=int(sys.argv[1])
soquete.bind((hospedeiro,porta))
print ('soquete colocado na porta '+ str(porta) +' do local '+ hospedeiro)
#precisamos esperar os 4 jogadores
soquete.listen(4)

#jogadores = []
#mao_jogadores=[]

#actualGame = jogo(jogadores, mao_jogadores, C_jogadas)
#divisão dos jogadores em times
#time1 = []
#time2= []
while 1:
    if gamestate==0:
        actualGame = jogo()
        i=0

        while 1:
        #O servidor fica aguardando as conexoes aqui
            Scliente, addr=soquete.accept()
            print ('o cliente %s parece ter conectado'%str(addr[i]))
        #jogadores.append(Scliente)#para mensagens gerais

            actualGame.jogadores.append(Scliente)
            manda_um(actualGame.jogadores[i],'N',str(i))
        #aviso=encode('N',str(i))
        #actualGame.jogadores[i].sendall(aviso.encode('utf-8'))
            i=i+1
            if i%2==1:#separa os jogadores em duplas pra facilitar comunicação
                actualGame.time1.append(Scliente)
            else:
                actualGame.time2.append(Scliente)
        #aviso=('voce e o jogador :%d:. aguarde todos os jogadores conectarem'% i)

            if i==2:#alterar para jogar com o numero certo de pessoas
                break
        msg='\n o jogo iniciara agora.'
        broadcast(actualGame.jogadores, msg)
        gamestate=gamestate+1
    if gamestate==1:
        actualGame.baralho = cria_baralho()
        random.shuffle(actualGame.baralho)
        actualGame.mao_jogadores,vira = distribui_cartas(actualGame.jogadores, actualGame.mao_jogadores, actualGame.baralho)
        print(actualGame.mao_jogadores)
        actualGame.vira=[vira[0], vira[1]]
        msg='O vira desta mão é %s de %s'%(vira[0],vira[1])
        print('aguardando um momento')
    #jogadores[0].send(msg.encode('utf-8'))
    #jogadores[1].send(msg.encode('utf-8'))
    #jogadores[0].send(encode('M',0,msg))
        broadcast(actualGame.jogadores, msg)
        gamestate=gamestate+1
    #a partir daqui, devem ser pedidas as entradas especificas de cada jogador
    if gamestate>=1:
        while 1:
        #ta estranho mas não vou mudar o de baixo

        #broadcast(actualGame.jogadores, encode('V', str(actualGame.atual)))
            notificacao = 'É a vez de %s'%actualGame.atual
            broadcast(actualGame.jogadores,notificacao)
            notif=encode('V',str(actualGame.atual)).encode('utf-8')
            actualGame.jogadores[actualGame.atual].sendall(notif)
        #recebido=actualGame.jogadores[actualGame.atual].recv(8192)
            recebido=receber(actualGame.jogadores[actualGame.atual],fila)
            decodeSvr(recebido, actualGame)
            actualGame.proxJogador()
            if actualGame.atual==2:
                break
        print(actualGame.Cartas_jogadas)
        resp=compara(actualGame.Cartas_jogadas[0],actualGame.Cartas_jogadas[1],actualGame.Cartas_jogadas[2],actualGame.Cartas_jogadas[3],vira)
        print(resp)

        #msg= ('V:%s: '% str(atual))
        #jogadores[atual].send(msg.encode('utf-8'))
        #while esperando:
        #    escolha=soquete.recv(8192)
        #   if escolha[1]== addr[atual]:
        #      opcoes=escolha[0].decode('utf-8')
