from collections import deque

def receber(fila):
    msg = ""
    if len(fila) != 0:
        while 'Ç' not in msg:
            msg += fila.pop()
            # se fila.pop() soltar IndexError, é pq não tem uma msg completa na fila e é pra ouvir mensagens
        msg.split('Ç')
        return msg[0]

    #caso não tenha uma mensagem terminada na fila
    while 1:
        msg += "JKSALFHWEFHASFSDFÇSDFOHWESADF" #é pra dar listen no sockete aqui
        if 'Ç' in msg:
            msg.split('Ç')
            for i in range (2, len(msg), 1):
                fila.append(msg[i])
            return msg[0]
