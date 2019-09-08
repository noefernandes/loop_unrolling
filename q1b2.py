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

t_start = 0
t_end = 0

# Cria a mémoria compartilhada
memory = posix_ipc.SharedMemory(SMEM_NAME, flags = posix_ipc.O_CREAT, mode = 0o777, size = 50)
mm_results = mmap.mmap(memory.fd, memory.size)
memory.close_fd()
#Cria o semáforo
sem = posix_ipc.Semaphore(SEM_NAME, flags = posix_ipc.O_CREAT, mode = 0o777,  initial_value=1)

#Lista que armazena os resultados retornados da funcao func.
height_a = 0
width_a = 0
height_b = 0
width_b = 0
results = []

#Funcao que efetua a operacao em cada elemento da matriz em uma thread.

def proc_func(row_a, mat_b, i):
	result =  np.zeros(width_b, dtype=np.uint32)
	for j in range(width_b):
		result[j] = np.sum(row_a*mat_b[:,j])
	pos = 4*i*width_a
	mm_results.seek(pos)
	bresult = result.tobytes() 
	# inicio da área protegida
	sem.acquire()
	mm_results.write(bresult)
	sem.release()
	# fim da área protegida
	sem.close()
	

def thread_func(row_a, mat_b, results, i):
	for j in range(width_b):
		results[i][j] = np.sum(row_a*mat_b[:,j])

def unroll(args, func, method, results):
	if method == 'proc':# todo
		sem.release()
		t_start = time.process_time()
		# controle de processos
		procs = []
		for i in range(height_a):
			proc = os.fork()
			if proc == 0:
				func(args[0][i], args[1], i)
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
		results = np.frombuffer(mm_results.read(4*height_a*width_b), dtype=np.uint32, count=height_a*width_b) 
		results.shape = (height_a,width_b)
		# print(args[0], '\n+\n', args[1], '\n=\n', results)
		print(t_end - t_start)
	elif method == 'thre':
		t_start = time.process_time()
		threads = []
		results = np.zeros((height_a, width_b), dtype=np.uint32)
		for i in range(height_a):
			x = threading.Thread(target=func, args=(args[0][i], args[1], results, i))
			threads.append(x)
			x.start()
		for t in threads:
			t.join()
		t_end = time.process_time()
		# print(args[0], '\nX\n', args[1], '\n=\n', results)
		print(t_end - t_start)
if (__name__ == "__main__"):
	if(width_a != height_b):
		print('A matriz não pode ser multiplicada, pois a largura de a:{} != altura de b:{}.'.format(width_a,height_b))
		exit(1)
	# Cria a mémoria compartilhada e o semaforo
	memory = posix_ipc.SharedMemory(SMEM_NAME, flags = posix_ipc.O_CREAT, mode = 0o777, size=100*100*4)
	mm_results = mmap.mmap(memory.fd, memory.size)
	memory.close_fd()
	sem = posix_ipc.Semaphore(SEM_NAME, flags = posix_ipc.O_CREAT, mode = 0o777,  initial_value=0)
	for i in range(101):
		if(i in [1, 2, 3, 4, 5, 6, 8, 10, 20, 30, 40, 50, 75, 100]):
			matrizA = np.random.randint(1, np.iinfo(np.uint16).max, (i,i), np.uint16)
			matrizB = np.random.randint(1, np.iinfo(np.uint16).max, (i,i), np.uint16)
			height_a, width_a, height_b, width_b = i, i, i, i
			# unroll([matrizA, matrizB], thread_func, 'thre', results)
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
