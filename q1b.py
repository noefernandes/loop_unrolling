# -*- coding: utf-8 -*-
import os
import mmap
import posix_ipc
import sys
import threading

SMEM_NAME = "smlu"


# Cria a mémoria compartilhada
memory = posix_ipc.SharedMemory(SMEM_NAME, flags = posix_ipc.O_CREAT, mode = 0o777, size = 50)
mm_results = mmap.mmap(memory.fd, memory.size)
memory.close_fd()
#Cria o semáforo
sem = posix_ipc.Semaphore("test_sem", flags = posix_ipc.O_CREAT, mode = 0o777,  initial_value=1)


#Lista que armazena os resultados retornados da funcao func.
results = []
height = 0
width = 0


#Funcao que efetua a operacao em cada elemento da matriz em uma thread.
def proc_func(args, pos):
    result = sum(args)
    print(result)
    # inicio da área protegida
    sem.acquire()
    mm_results[pos:pos+4] = result.to_bytes(4,byteorder='big')
    sem.release()
    # fim da área protegida

#Funcao que efetua a operacao em cada elemento da matriz em um processo
def thread_func(ele_a, ele_b, results, i, j):
    results[i][j] = ele_a + ele_b


def unroll(args, func, method, results):
    len_args = len(args)
    if method == 'proc':
        mm_results.seek(0)
        for i in range(len_args):
            if os.fork() == 0:
                func(args[i], i*4)
                os._exit(0)
        # Espera todos os processos filho terminarem
        for _ in range(len_args):
            os.waitpid(0, 0)
        # Imprimi o resultado
        print([int.from_bytes(mm_results.read(4), byteorder='big') for _ in range(len_args)])
    elif method == 'thre':
        threads = []
        results = [None] * height
        for i in range(height):
            results[i] = [None] * width      

        for i in range(height):
            results[i] = [None] * width
            for j in range(width):
                x = threading.Thread(target=func, args=(args[0][i][j], args[1][i][j], results, i, j))
                threads.append(x)
                x.start()

        for t in threads:
            t.join()
        print(results)

if (__name__ == "__main__"):
    matrizA = [[1,2,3],[4,5,6]]
    matrizB = [[7,8,9],[10,11,12]]

    height = len(matrizA)
    width = len(matrizA[0])

    unroll([matrizA, matrizB], thread_func, 'thre', results)
    sem.close()
    mm_results.close()
    posix_ipc.unlink_shared_memory(SMEM_NAME)


#Para testar quantidade de threads ativas.
#print(threading.activeCount())


''' Referencias
https://docs.python.org/3.7/library/os.html
https://docs.python.org/3.7/library/mmap.html
https://docs.python.org/3/library/stdtypes.html
'''