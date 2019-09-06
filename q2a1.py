# -*- coding: utf-8 -*-
import time

t_start = time.process_time()

height_a = 0
width_a = 0
height_b = 0
width_b = 0

def mat_product(args, results):
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
	print(results)

if (__name__ == "__main__"):
	results = []
	matriz_a = [[3,2],[3,3], [1,2]]
	matriz_b = [[3,2,6],[1,2,5]]
	height_a = len(matriz_a)
	height_b = len(matriz_b)
	width_a = len(matriz_a[0])
	width_b = len(matriz_b[0])
	if(width_a != height_b):
		print('A matriz não pode ser multiplicada, pois a largura de a:{} != altura de b:{}.'.format(width_a,height_b))
		exit(1)
	mat_product([matriz_a, matriz_b],results)
	t_end = time.process_time()
	print(t_end - t_start)

#Para testar quantidade de threads ativas.
#print(threading.activeCount())


''' Referencias
https://docs.python.org/3.7/library/os.html
https://docs.python.org/3.7/library/mmap.html
https://docs.python.org/3/library/stdtypes.html
'''
