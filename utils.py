import time
import matplotlib.pyplot as plt

def plot_convergence(history, algo_name):
    plt.plot(history)
    plt.title(f"Convergence - {algo_name}")
    plt.xlabel("Iteration")
    plt.ylabel("Best Fitness")
    plt.grid(True)
    plt.show()

def timeit(func, *args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    return end - start, result