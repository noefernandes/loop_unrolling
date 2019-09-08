# -*- coding: utf-8 -*-
import time
import numpy as np

height_a = 0
width_a = 0
height_b = 0
width_b = 0

def mat_sum(args, results):
	t_start = time.process_time()
	results = np.zeros((width_a, height_a), dtype=np.uint32)
	for i in range(height_a):
		results[i] = args[0][i] + args[1][i]
	t_end = time.process_time()
	print(t_end - t_start)

def mat_product(args, results):
	t_start = time.process_time()

	results =  np.zeros((width_a, height_a), dtype=np.uint32)
	for i in range(height_a):
		for j in range(width_b):
			results[i] = np.sum(args[0][i]*args[1][:j])
	t_end = time.process_time()
	print(t_end - t_start)

if (__name__ == "__main__"):
	results = []
	if(width_a != height_b):
		print('A matriz não pode ser multiplicada, pois a largura de a:{} != altura de b:{}.'.format(width_a,height_b))
		exit(1)

	#para testar os tempos de execução da operação para cada ordem de matriz.
	for i in [1, 2, 3, 4, 5, 6, 8, 10, 20, 30, 40, 50, 75, 100]:
		matrizA = np.random.randint(0, np.iinfo(np.uint16).max, (i,i), np.uint16)
		matrizB = np.random.randint(0, np.iinfo(np.uint16).max, (i,i), np.uint16)
		height_a, width_a, height_b, width_b = i, i, i, i
		mat_sum([matrizA, matrizB],results)
		# mat_product([matrizA, matrizB],results)


''' Referencias
https://docs.python.org/3.7/library/os.html
https://docs.python.org/3.7/library/mmap.html
https://docs.python.org/3/library/stdtypes.html
'''
