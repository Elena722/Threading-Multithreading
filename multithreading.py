'''1. Create the following functions:
1. generate_random(out_q, n) which generates n random integers and puts them in out_q Queue
2. square(in_q, out_q, n) which takes numbers from the in_q Queue and puts their squares in the out_q.
3. to_binary(in_q, out_q, n) takes numbers from the in_q Queue and puts their binary representations in the
out_q.
2. Create the three queues needed to connect functions in the following order:
1. generate_random 2. queue_a
3. square
4. queue_b
5. to_binary
6. result_q
3. Run the three functions in separate processes. Make generate_random generate 1000 integers.
4. Important! Read all the items from result_q before calling .join()
5. You can add timeout=<seconds> to put/get calls to avoid deadlocks.'''

import random
import multiprocessing

def generate_random(out_q, n):  # n =1000  out_q = queue_a
    for _ in range(n):
        out_q.put(random.randint(1, 100))  # fill in queue_a

def square(in_q, out_q, n):  # queue_a, queue_b
    for _ in range(n):
        x = in_q.get()  # after for loop queue_a is going to be empty
        out_q.put(x**2)  # fill in queue_b

def to_binary(in_q, out_q, n):   # in_q = queue_b  out_q = result_q
    for _ in range(n):
        y = in_q.get()  # after for loop queue_b is going to be empty
        out_q.put(bin(y))  # fill in result_q

if __name__=='__main__':
    queue_a = multiprocessing.Queue(maxsize=1000)
    queue_b = multiprocessing.Queue(maxsize=1000)
    result_q = multiprocessing.Queue(maxsize=1000)

    processes = [
        multiprocessing.Process(target=generate_random, args=(queue_a, 1000)),
        multiprocessing.Process(target=square, args=(queue_a, queue_b, 1000)),
        multiprocessing.Process(target=to_binary, args=(queue_b, result_q, 1000)),
    ]
    for p in processes:
        p.start()
    res = []
    for i in range(1000):
        x = result_q.get()
        res.append(x)
    for p in processes:
        p.join()

    print(res[:10])

