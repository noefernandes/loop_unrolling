# -*- coding: utf-8 -*-
import threading
from collections import deque
from random import randrange
''' Para fazer
- Olhar a seguinte implementação: https://docs.python.org/3/library/queue.html
- Colocar a operação paralela que já foi feita e utilizar no multiplicar_par
- Olhar a modelagem na rede de petri e colocar o semaforo
	
'''


fila_de_matrizes = deque()

def multiplicar_par(a, b, predecessor_lock):
	# proteger a mémoria
	# se tiver 1 na fila manda o sinal

	# if(len(deque) > 0): # manda o sinal
	# predecessor_lock.aquire()
	# 
	'''
	def unroll(args, func, results):
		threads = []

		results = [None] * height_a
		for i in range(height_a):
			results[i] = [None] * width_b
			for j in range(width_b):
				x = threading.Thread(target=func, args=(results,i,j))
				threads.append(x)
				x.start()
		for t in threads:
			t.join()	
		print(results)
	from random import randrange'''

def gerar_matriz(height, width, range_start, range_end):
	matriz = [None]*height
	for i in range(height):
		matriz[i] = [None]*width
		for j in range(width):
			matriz[i][j] = randrange(range_start, range_end)
	return matriz

def gerar_matrizes_multiplicativas(amount, min_height = 2, min_width = 2, max_height = 5, max_width = 5,
									range_start = 0, range_end=10):
	matrizes = deque()
	height = randrange(min_height, max_height)
	for n in range(amount):
		width = randrange(min_width, max_width)
		matrizes.append(gerar_matriz(height, width, range_start, range_end))
		height = width
	return matrizes

def print_multi_one_digit(matrizes, cols):
	height = max([len(mat) for mat in matrizes])
	sep = ' x '
	for i in range(height):
		print(sep.join(filter(lambda x: x != None, [
								str(matrizes[col][i]) if i < len(matrizes[col]) else None 
								for col in range(cols)])))
		sep = '   '

if (__name__ == '__main__'):
	# ABCDE
	# AB
	# CD
	# E
	# AB CD E
	# mandar lock do antecessor
	# gerar conjunto de matrizes
	# 4x3 * 3x2 * 2x5 * 5*4
	# 2x3 * 4x2 * 5x2
	print_multi_one_digit(gerar_matrizes_multiplicativas(2), 2)