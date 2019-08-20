import os
import time

def func(args):
    print(a, b)

print("processo pai")
def unroll(args, func, method, results):
    if(method == 'proc'):
        for i in range(len(args)): # loop will run n times (n=5)
            if(os.fork() == 0):
                print("[son] pid {0} from [parent] pid {1}\n".format(os.getpid(),os.getppid()));
                os._exit(0)
        for i in range(len(args)):
            os.wait()

results = []
unroll([1, 2, 3], func, 'proc', results)
