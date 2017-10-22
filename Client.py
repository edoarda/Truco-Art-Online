import socket
import sys

#1,2,3,4
def encode(letra,Nplayer,carta=' '):
    msg = letra+':'+Nplayer+':'+carta
    return msg

def decodeClnt (codigo, numjogador):
    guarda=codigo.split(':')
    if guarda[0]=='M':
        print(guarda[2])
    
    elif guarda[0] == 'V' and guarda[1] == numjogador:
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

    elif guarda[0] == 'T' and guarda[1] != numjogador:
        #caso tenha recebido a mensagem do truco
        print("Jogador " + guarda[1] + "pediu truco. O que você faz?\n")
        resp = input("Escolha sua ação:\n 1-RETRUCAR!!!\n 2-Aceitar\n 3-Fugir\n")
        #send (T resp)

#tentar criar um socket
c_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print ('soquete criado')
#eis aqui a porta de destino
destino=sys.argv[1]
porta=int(sys.argv[2])
mao=[]
print ('tentando acessar a porta '+ str(porta) +' do local '+ destino)
#precisamos esperar os 4 jogadores
c_sock.connect((destino,porta))
print ('conectado ao servidor')
baite=c_sock.recv(1024)
aviso=baite.decode('utf-8')
numjogador = aviso.split(':')
numjogador = numjogador[1]
print (aviso)
msg=c_sock.recv(1024)
print (msg.decode('utf-8'))
msg=c_sock.recv(1024)
print (msg.decode('utf-8'))
pilo=msg.decode('utf-8')
cartaS=pilo.split(' ',6)
for i in range(0,6,2):
    carta=(cartaS[i],cartaS[i+1])
    mao.append(carta)
    print(mao[0][1])


while 1:
    msg=c_sock.recv(1024)
    segura=(msg.decode('utf-8'))
    decodeClnt (segura, numjogador)
