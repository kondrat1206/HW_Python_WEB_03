import timeit
from multiprocessing import Process, Queue

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = timeit.default_timer()
        result = func(*args, **kwargs)
        end_time = timeit.default_timer()
        execution_time = end_time - start_time
        print(f"{func.__name__} execution time: {execution_time} seconds")
        return result
    return wrapper

@timing_decorator
def factorize(*numbers):
    result = []
    for num in numbers:
        factors = [i for i in range(1, num + 1) if num % i == 0]
        result.append(factors)
    return result


def factorize_single(num, result_queue):
    factors = [i for i in range(1, num + 1) if num % i == 0]
    result_queue.put(factors)

@timing_decorator
def factorize_mult(*numbers):
    result_queue = Queue()
    processes = []

    for num in numbers:
        process = Process(target=factorize_single, args=(num, result_queue))
        processes.append(process)
        process.start()
        print(processes)

    for process in processes:
        process.join()

    result = [result_queue.get() for _ in numbers]
    return result



if __name__ == "__main__":

    a, b, c, d = factorize(12899899, 25588345, 99999856, 10651060)

    # assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    # assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    # assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    # assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    a, b, c, d = factorize_mult(12899899, 25588345, 99999856, 10651060)

    # assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    # assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    # assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    # assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]


