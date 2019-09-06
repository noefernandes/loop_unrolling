# -*- coding: utf-8 -*-
import time
import numpy as np

height_a = 0
width_a = 0
height_b = 0
width_b = 0

def mat_product(args, results):
	t_start = time.process_time()
	soma = 0
	matriz_a = args[0]
	matriz_b = args[1]
	results = [None] * height_a
	for i in range(height_a):
		results[i] = [None] * width_b
		for j in range(width_b):
			soma = 0
			for k in range(width_a):
				soma += matriz_a[i][k]*matriz_b[k][j]
			results[i][j] = soma
	t_end = time.process_time()
	print("tempo: " + str(t_end - t_start))
	#print("tamanho da matriz: " + str(height_a) + "\n")

if (__name__ == "__main__"):
	results = []
	#matriz_a = [[3,2],[3,3], [1,2]]
	#matriz_b = [[3,2,6],[1,2,5]]
	#height_a = len(matriz_a)
	#height_b = len(matriz_b)
	#width_a = len(matriz_a[0])
	#width_b = len(matriz_b[0])
	if(width_a != height_b):
		print('A matriz não pode ser multiplicada, pois a largura de a:{} != altura de b:{}.'.format(width_a,height_b))
		exit(1)

	#para testar os tempos de execução da operação para cada ordem de matriz.
	for i in [1, 2, 3, 4, 5, 6, 8, 10, 20, 30, 40, 50, 75, 100]:
		matriz_a = np.random.randint(5, size = (i, i))
		matriz_b = np.random.rand(i, i)
		height_a = len(matriz_a)
		height_b = len(matriz_b)
		width_a = len(matriz_a[0])
		width_b = len(matriz_b[0])
		mat_product([matriz_a, matriz_b],results)

#Para testar quantidade de threads ativas.
#print(threading.activeCount())


''' Referencias
https://docs.python.org/3.7/library/os.html
https://docs.python.org/3.7/library/mmap.html
https://docs.python.org/3/library/stdtypes.html
'''
