# -*- coding: utf-8 -*-
import threading
from collections import deque
from random import randrange
import numpy as np

fila_de_matrizes = deque()

def multiplicar_par(a, b, current, predecessor):
	result = a.dot(b)
	predecessor.acquire()
	print(str(len(a)) + 'x' + str(len(a[0])), '·', str(len(b)) + 'x' + str(len(b[0])))
	matrizes.append(result)
	current.release()
def unroll(matrizes):
	print(" · ".join(str(len(m)) + 'x' + str(len(m[0])) for m in matrizes))
	print('=')
	while(len(matrizes) > 1):
		lock = threading.Lock()
		n = len(matrizes)
		while(n > 1):
			prev = lock
			lock = threading.Lock()
			lock.acquire()
			thread = threading.Thread(target=multiplicar_par, args=(matrizes.popleft(), matrizes.popleft(), lock, prev))
			thread.start()
			n -= 2
		lock.acquire()
		if(n == 1):
			matrizes.append(matrizes.popleft())
		print('=')
	print(str(len(matrizes[0]))+'x'+str(len(matrizes[0][0])))

def gerar_matrizes_multiplicativas(amount, min_height = 1, min_width = 1, max_height = 5, max_width = 5,
									range_start = 0, range_end=10):
	matrizes = deque()
	height = randrange(min_height, max_height+1)
	for n in range(amount):
		width = randrange(min_width, max_width+1)
		matrizes.append(np.random.randint(0, np.iinfo(np.uint8).max+1, (height,width), np.uint8))
		height = width
	return matrizes
if (__name__ == '__main__'):
	matrizes = gerar_matrizes_multiplicativas(7, max_width=30, max_height=30)
	output = '\n·\n'.join(str(mat) for mat in matrizes)
	unroll(matrizes)
	print(output)
	print('=')
	print(matrizes[0])