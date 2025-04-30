# test_multiprocessing.py
import multiprocessing
import time

def process_function(number):
    return number * number

if __name__ == '__main__':
    start_time = time.time()
    
    # Sequential processing
    results_seq = [process_function(i) for i in range(1000000)]
    seq_time = time.time() - start_time
    print(f"Sequential time: {seq_time:.2f} seconds")
    
    # Parallel processing
    start_time = time.time()
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results_parallel = pool.map(process_function, range(1000000))
    parallel_time = time.time() - start_time
    print(f"Parallel time: {parallel_time:.2f} seconds")
    print(f"Speedup: {seq_time/parallel_time:.2f}x")