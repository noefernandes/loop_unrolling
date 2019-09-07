# -*- coding: utf-8 -*-
import os
import mmap
import posix_ipc
import sys
import threading
import time
import numpy as np

SMEM_NAME = "smlu"
SEM_NAME = "semlu"


#Lista que armazena os resultados retornados da funcao func.
results = []
height = 0
width = 0
t_start = 0
t_end = 0

#Funcao que efetua a operacao em cada elemento da matriz em uma thread.
def proc_func(row_a, row_b, i):
	result = row_a + row_b
	pos = i*width*4
	# inicio da área protegida
	mm_results.seek(pos)
	sem.acquire()
	mm_results.write(result.tobytes())
	sem.release()
	sem.close()
	# fim da área protegida

#Funcao que efetua a operacao em cada elemento da matriz em um processo
def thread_func(ele_a, ele_b, results, i, j):
	results[i][j] = ele_a + ele_b

def unroll(args, func, method, results):
	if method == 'proc':
		sem.release()
		t_start = time.process_time()
		# controle de processos
		procs = []
		for i in range(height):
			proc = os.fork()
			if proc == 0:
				func(args[0][i], args[1][i], i)
				os._exit(0)
			else:
				procs.append(proc)
		# Espera todos os processos filho terminarem
		for proc in procs:
			os.waitpid(proc, 0)
		t_end = time.process_time()
		sem.acquire()
		
		mm_results.seek(0)
		# Exibir o resultado
		results = np.zeros((width, height))
		for i in range(height):
			for j in range(width):
				results[i][j] = int.from_bytes(mm_results.read(4), byteorder='big')
		print(args[0], '+\n', args[1], '=\n', results)
		
		print(t_end - t_start)
	elif method == 'thre':
		t_start = time.process_time()
		threads = []
		results = np.zeros((width, height)).tolist()
		for i in range(height):
			for j in range(width):
				x = threading.Thread(target=func, args=(args[0][i][j], args[1][i][j], results, i, j))
				threads.append(x)
				x.start()
		for t in threads:
			t.join()
		t_end = time.process_time()
		# print(args[0], '+', args[1], '=', results)
		print(t_end - t_start)

if (__name__ == "__main__"):
	# Cria a mémoria compartilhada e o semaforo
	memory = posix_ipc.SharedMemory(SMEM_NAME, flags = posix_ipc.O_CREAT, mode = 0o777, size=100*100*4)
	mm_results = mmap.mmap(memory.fd, memory.size)
	memory.close_fd()
	sem = posix_ipc.Semaphore(SEM_NAME, flags = posix_ipc.O_CREAT, mode = 0o777,  initial_value=0)
	# Controla os testes
	for i in [1, 2, 3, 4, 5, 6, 8, 10]:
		matrizA = np.random.randint(0,100,(i,i), 'int')
		matrizB = np.random.randint(0,100,(i,i), 'int')
		height, width = i, i
		unroll([matrizA, matrizB], proc_func, 'proc', results)
	# Fecha a mémoria
	sem.unlink()
	mm_results.close()
	posix_ipc.unlink_shared_memory(SMEM_NAME)



''' Referencias
https://docs.python.org/3.7/library/os.html
https://docs.python.org/3.7/library/mmap.html
https://docs.python.org/3/library/stdtypes.html
'''
