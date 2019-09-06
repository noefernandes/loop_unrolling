# -*- coding: utf-8 -*-
import os
import mmap
import posix_ipc
import sys
import threading
import time
import numpy as np

SMEM_NAME = "smlu"

t_start = 0
t_end = 0

# Cria a mémoria compartilhada
memory = posix_ipc.SharedMemory(SMEM_NAME, flags = posix_ipc.O_CREAT, mode = 0o777, size = 50)
mm_results = mmap.mmap(memory.fd, memory.size)
memory.close_fd()
#Cria o semáforo
sem = posix_ipc.Semaphore("test_sem", flags = posix_ipc.O_CREAT, mode = 0o777,  initial_value=1)


#Lista que armazena os resultados retornados da funcao func.
results = []
height_a = 0
width_a = 0
height_b = 0
width_b = 0

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

def thread_aux(results, k, i, j):
	results[k] = matriz_a[i][k]*matriz_b[k][j]

def thread_func(results, i, j):
	results_partial = [None] * width_a
	threads = []
	for k in range(width_a):
		x = threading.Thread(target=thread_aux, args=(results_partial, k, i, j))
		threads.append(x)
		x.start()
	for t in threads:
		t.join()
	results[i][j] = sum(results_partial)

def unroll(args, func, method, results):
	len_args = len(args)
	if method == 'proc':
		t_start = time.process_time()
		mm_results.seek(0)
		for i in range(len_args):
			if os.fork() == 0:
				func(args[i], i*4)
				os._exit(0)
		# Espera todos os processos filho terminarem
		for _ in range(len_args):
			os.waitpid(0, 0)
		t_end = time.process_time()
		# Imprime o resultado
		print('%f' % (t_end - t_start))
		print([int.from_bytes(mm_results.read(4), byteorder='big') for _ in range(len_args)])
	elif method == 'thre':
		t_start = time.process_time()
		threads = []
		matriz_a = args[0]
		matriz_b = args[1]
		results = [None] * height_a
		for i in range(height_a):
			results[i] = [None] * width_b
			for j in range(width_b):
				x = threading.Thread(target=func, args=(results,i,j))
				threads.append(x)
				x.start()
		for t in threads:
			t.join()
		t_end = time.process_time()
		print(t_end - t_start)
		#print('%f' % (t_end - t_start))

if (__name__ == "__main__"):
	#matriz_a = [[3,2],[3,3], [1,2]]
	#matriz_b = [[3,2,6],[1,2,5]]
	#height_a = len(matriz_a)
	#height_b = len(matriz_b)
	#width_a = len(matriz_a[0])
	#width_b = len(matriz_b[0])
	if(width_a != height_b):
		print('A matriz não pode ser multiplicada, pois a largura de a:{} != altura de b:{}.'.format(width_a,height_b))
		exit(1)

	#unroll([matriz_a, matriz_b], thread_func, 'thre', results)

	for i in range(101):
		if(i in [1, 2, 3, 4, 5, 6, 8, 10, 20, 30, 40, 50, 75, 100]):
			matrizA = np.random.rand(i,i).tolist()
			matrizB = np.random.rand(i,i).tolist()
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
