import subprocess
from deap import benchmarks

NTHREADS_MIN = 1
NTHREADS_MAX = 240
INVALID_NTHREADS_PENALTY = 1000.0
NUM_TEAMS = 4

def run(params):
    return benchmarks.ackley(params)
    #return exec_benchmark(params)


def exec_benchmark(params):
    # command in form ['app', 'arg1', 'arg2',..]
    command = ['ls', '-l']
    process = subprocess.run(command, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    # Get results from stdout, application is asummed to return the execution time
    exec_time = float(process.stdout)
    return exec_time


# Check if individual is not out-of-bond,
# i.e., number of threads is invalid
def feasible(params):
    """Feasibility function for the individual. Returns True if feasible False
        otherwise."""
    valid = True
    for nthreads in params:
        if nthreads < NTHREADS_MIN or nthreads > NTHREADS_MAX:
            valid = False
            break

    return valid
