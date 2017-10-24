import sys
import socket


#funçoes implementadas

#função para pegar mensagens enviadas garantir que é só uma mensagem mesmo
# função que vai recebendo coisas, separa bonitinho no caso do python ter sido um amorzinho e peidado nas mensagens e taca o que sobrou numa fila
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

def encode(letra,Nplayer,carta=' '):
    msg = letra+':'+Nplayer+':'+carta + '@Ç'
    return msg

#Mensagens que podem ser recebidas pelo cliente
# Cabeçalho M = mensagens gerais
# Cabeçalho N = Numero do jogador
# Cabeçalho V = Vez do cliente
# Cabeçalho C = Cartas deste cliente
# Cabeçalho T = Pedido de truco inimigo
# Cabeçalho E = Fim do jogo
#Mensagens Enviadas pelo cliente
# Cabeçalho A = Jogar carta aberta
# Cabeçalho F = Jogar carta fechada
# Cabeçalho T = Pedir Truco
# Cabeçalho K = Aceitar truco
# Cabeçalho D = Fugir do truco
# Cabeçalho R = Pedido Retruco

def decodeClnt (deco,mao,numjogador):
    #deco = codigo.decode('utf-8')
    msg=deco.split(':')
    if msg[0]=='N':
        numjogador = msg[1]
        print ('Você é o jogador :%s:'%numjogador)
    elif msg[0]=='M':
        print(msg[2])
    elif msg[0]=='V':
        print('É a sua vez')
        print("Escolha sua ação:\n 1-Jogar carta aberta\n 2-Jogar carta fechada\n 3-Pedir truco\n")
        resp=input("responda com o numero correspondente:")
        if int(resp)==1:
            print ('Escolha a carta a ser jogada:')
            for i in range (0,len(mao)):#loop para botar as opções na tela
                print('%s- %s de %s '% (str(i), mao[i][0], mao[i][1]))
            resp2=input("responda com o numero correspondente a carta escolhida")
            opcao=mao.pop(int(resp2))
            msg=encode('A',str(numjogador),resp2)
            print('A',numjogador,resp2)
        if int(resp)==2:
            print ('Escolha a carta a ser jogada:')
            for i in range (0,len(mao)):#loop para botar as opções na tela
                print('%s- %s de %s '% (str(i), mao[i][0], mao[i][1]))
            resp2=input("responda com o numero correspondente a carta escolhida")
            opcao=mao.pop(int(resp2))
            msg=encode('F',numjogador,resp2)
            print('F',numjogador,resp2)
        c_sock.send(msg.encode('utf-8'))
    elif msg[0]=='W':
        #Receber as cartas e salvar
        for i in range(1,7,2):
            carta=(msg[i],msg[i+1])
            mao.append(carta)
            print(mao[0][1])
    elif msg[0]=='T':
        print('Ainda tem que fazer o truco')
        #caso tenha recebido a mensagem do truco
        print("Jogador " + msg[1] + "pediu truco. O que você faz?\n")
        resp = input("Escolha sua ação:\n 1-RETRUCAR!!!\n 2-Aceitar\n 3-Fugir\n")
        if int(resp) == 1 or resp.upper == 'RETRUCAR':
            print("Voce pediu retruco")
            encode('R',numjogador,' ')
        elif int(resp) == 2 or resp.lower == 'aceitar':
            print("Voce aceitou o truco do seu oponente")
            encode('K',numjogador,' ')
        else:
            if int(resp) == 3 or resp.lower == 'fugir':
                print('Voce fugiu')
            else:
                print('Resposta fora dos padrões, foi considerado como fugir')
            encode('D',numjogador,' ')
        #send (T resp)
    elif msg[0]=='E':
        print("O Jogo Terminou!! Deseja Continuar Jogando? :\n S-SIM\n N-NÃO\n")
        resp=input("responda com a letra correspondente:")
        if resp=='Y' or resp.lower=='y':
            print("Aguarde os outros jogadores")
        elif resp=='N' or resp.lower=='n':
            print("Obrigado por jogar")
            #encerrar conexão, fazer ainda
        else:
            print("Comando desconhecido, Encerrando jogo.......")
            #Encerrar
            exit()


#Conectar servidor:
#tentar criar um socket
c_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print ('soquete criado')
#eis aqui a porta de destino
destino=sys.argv[1]
porta=int(sys.argv[2])
mao=[]
numjogador=-1
fila=[]
print ('tentando acessar a porta '+ str(porta) +' do local '+ destino)
#precisamos esperar os 4 jogadores
c_sock.connect((destino,porta))
print ('conectado ao servidor')

while 1:
    print(fila)
    #loop de jogo
    #aguardar resposta
    #recebido=c_sock.recv(8192)
    #decodeClnt(recebido)
    if len(fila)==0:
        recebido = receber(c_sock,fila)
    else:
        recebido = fila.pop()
        if '@' in recebido: # msg tem fim. yay!
            recebdo = recebido.split('@')
            print(fila)
    decodeClnt(recebido,mao,numjogador)
    print('Terminando loop')
