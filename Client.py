import socket
import sys

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
aviso=c_sock.recv(1024)
print (aviso.decode('utf-8'))
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

msg=c_sock.recv(1024)
print (msg.decode('utf-8'))
while 1:
    #cria
    msg=c_sock.recv(1024)
    print("Escolha sua ação:\n 1-Jogar carta aberta\n 2-Jogar carta fechada\n 3-Pedir truco\n")
    resp=input("responda com o numero correspondente:")
    if int(resp)==1 or int(resp)==2:
        print ('Escolha a carta a ser jogada:')
        for i in range (0,len(mao)):#loop para botar as opções na tela
            print('%s- %s de %s '% (str(i), mao[i][0], mao[i][1]))
        resp2=input("responda com o numero correspondente a carta escolhida")
        opcao=mao.pop(int(resp2) - 1)
        choice= resp +' '+ opcao[0]+' '+opcao[1]
    c_sock.send(choice.encode('utf-8'))
