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
results2 = []


def unroll(args, func, method, results, results2):
    if method == 'proc':
        size = len(args)
        i = 0
        while(i < size-1):
            if os.fork() == 0:
                results2.append(func(args[i]))
                print('2a', results2)
                os._exit(0)
            else:
                results.append(func(args[i+1]))
            i+=2
        if(i == size-1):
            results.append(func(args[i]))
        for _ in range(size//2):
            os.wait()
       # results += results2
        print('2b', results2)

    elif method == 'thre':
        threads = []
        for i in args:
            x = threading.Thread(target=thread_func, args=(i,))
            threads += [x]
            x.start()
            results.append(func(i))
        for t in threads:
            t.join()
            


unroll([[1,2],[3,4],[5,6]], func, 'proc', results, results2)
print(results)

#Para testar quantidade de threads ativas.
#print(threading.activeCount())