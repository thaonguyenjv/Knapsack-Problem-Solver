import time, importlib
import problem as p
from ga_solver import solve_ga
from woa_solver import WOA

DATA_DIR = 'data'

def run_single(algo, w, v, c, pop=50, iters=100, return_convergence=False):
    convergence = []
    start = time.time()
    if algo == 'GA':
        _, val, hist = solve_ga(w, v, c, pop, iters, 0.8, 0.01)
        if return_convergence:
            convergence = hist
    else:
        p.weights = w; p.values = v; p.capacity = c
        importlib.reload(__import__('woa_solver'))
        woa = WOA(pop, iters, len(w))
        _, val, hist = woa.optimize()
        if return_convergence:
            convergence = hist
    elapsed = time.time() - start
    return (val, elapsed, convergence) if return_convergence else (val, elapsed)