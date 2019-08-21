import os
import time
import threading

#Funcao que efetua a operacao em cada linha da matriz.
def func(args):
    return sum(args)

#Funcao de auxilio da thread.
def thread_func(args):
    t = threading.currentThread()
    print ("Sou o processo " + str(os.getpid()) + " na thread " + str(t.ident))

#Lista que armazena os resultados retornados da funcao func.
results = []


def unroll(args, func, method, results):
    if method == 'proc':
        for i in args:
            results.append(func(i))
            if os.fork() == 0:
                os._exit(0)
        for i in range(len(args)):
            os.wait()
    elif method == 'thre':
        for i in args:
            x = threading.Thread(target=thread_func, args=(i,))
            x.start()
            results.append(func(i))


unroll([[1,2],[3,4],[5,6]], func, 'thre', results)
print(results)

#Para testar quantidade de threads ativas.
#print(threading.activeCount())