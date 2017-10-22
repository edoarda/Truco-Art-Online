import sys
import socket


#funçoes implementadas


def encode(letra,Nplayer,carta=' '):
    msg = letra+':'+Nplayer+':'+carta
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



def decodeClnt (codigo,mao):
    deco = codigo.decode('utf-8')
    msg=deco.split(':')

    if msg[0]=='M':
        print(msg[2])
    elif msg[0]=='N':
        numero = msg[1]
        print ('Você é o jogador :%d:'%numero)
    elif msg[0]=='V':
        print('É a sua vez')
        print("Escolha sua ação:\n 1-Jogar carta aberta\n 2-Jogar carta fechada\n 3-Pedir truco\n")
        resp=input("responda com o numero correspondente:")
        if int(resp)==1:
            print ('Escolha a carta a ser jogada:')
            for i in range (0,len(mao)):#loop para botar as opções na tela
                print('%s- %s de %s '% (str(i), mao[i][0], mao[i][1]))
            resp2=input("responda com o numero correspondente a carta escolhida")
            opcao=mao.pop(int(resp2) - 1)
            msg=encode('A',numjogador,(resp2-1))
        if int(resp)==2:
            print ('Escolha a carta a ser jogada:')
            for i in range (0,len(mao)):#loop para botar as opções na tela
                print('%s- %s de %s '% (str(i), mao[i][0], mao[i][1]))
            resp2=input("responda com o numero correspondente a carta escolhida")
            opcao=mao.pop(int(resp2) - 1)
            msg=encode('F',numjogador,(resp2-1))
        c_sock.send(msg.encode('utf-8'))
    elif msg[0]=='C':
        #Receber as cartas e salvar
        for i in range(1,7,2):
            carta=(msg[i],msg[i+1])
            mao.append(carta)
            print(mao[0][1])
    elif msg[0]=='T':
        print('Ainda tem que fazer o truco')
        #caso tenha recebido a mensagem do truco
        #print("Jogador " + msg[1] + "pediu truco. O que você faz?\n")
        resp = input("Escolha sua ação:\n 1-RETRUCAR!!!\n 2-Aceitar\n 3-Fugir\n")
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
numjogador = []
print ('tentando acessar a porta '+ str(porta) +' do local '+ destino)
#precisamos esperar os 4 jogadores
c_sock.connect((destino,porta))
print ('conectado ao servidor')

while 1:
    #loop de jogo
    #aguardar resposta
    recebido=c_sock.recv(1024)
    decodeClnt(recebido)