import os
import time

def func(args):
    sum(args)

results = []
#print("processo pai")
def unroll(args, func, method, results):
    if(method == 'proc'):
        for i in range(len(args)):
            if(os.fork() == 0):
                #print("[son] pid {0} from [parent] pid {1}\n".format(os.getpid(),os.getppid()));
                results.append(func(args))
                os._exit(0)
        for i in range(len(args)):
            os.wait()
    elif(method == 'thre'):
    
unroll([1, 2, 3], func, 'proc', results)
