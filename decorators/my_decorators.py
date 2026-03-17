import tracemalloc
import time


def measure_time(func):
    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        stop = time.time() - start
        print(f"Time needed to complete task: {stop} for {",".join(map(str, args))}. ")
        return result 
    return inner

def measure_memory_alloc(func):
    def inner(*args, **kwargs):
        tracemalloc.start()
        result = func(*args, **kwargs)
        _, peak = tracemalloc.get_traced_memory()
        print(f"Memory peak is equal {peak} for {",".join(map(str, args))}. ")
        tracemalloc.stop()
        return result
    return inner

