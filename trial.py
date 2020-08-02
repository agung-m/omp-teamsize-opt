import subprocess
from deap import benchmarks
from nbody_runner import NBodyRunner

NTHREADS_MIN = 1
NTHREADS_MAX = 240
NUM_TEAMS = 4
# GA typically assume unbounded individuals, so we need to overcome bound problems 
# by using the feasibility function.
# Set penalty higher than the estmated max execution time of trials, or as high as possible,
# or we can get unbounded individuals.
#INVALID_NTHREADS_PENALTY = float('inf')
INVALID_NTHREADS_PENALTY = 1000000.0

nbody_workdir = '.'  # current workdir, or set to path of nbody dir
src_filename = "src/parallel/main.c"
temp_src_filename = 'src/parallel/main-4teams.c'
run_script = 'run_dubinsky.sh'

def run(params):
    #print("[Trial] {}".format(params))
    #return benchmarks.ackley(params)
    #return exec_benchmark(params)
    print("[Trial] {}".format(params))
    return exec_nbody(params),

def exec_benchmark(params):
    # command in form ['app', 'arg1', 'arg2',..]
    command = ['ls', '-l']
    process = subprocess.run(command, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    # Get results from stdout, application is asummed to return the execution time
    exec_time = float(process.stdout)
    return exec_time

def exec_nbody(params):
    nbody_runner = NBodyRunner(nbody_workdir, NUM_TEAMS, src_filename, temp_src_filename, run_script)
    exec_times = nbody_runner.execute_nbody(params)
    return exec_times[1]
    #nbody_runner.execute_nbody([60, 60, 60, 60])
    

# Check if individual is not out-of-bond,
# i.e., number of threads is invalid
def feasible(params):
    """Feasibility function for the individual. Returns True if feasible False
        otherwise."""
    #print(sum(params))
    valid = True
    # Check individual param first to avoid wrong sum
    for nthreads in params:
        #if nthreads < NTHREADS_MIN or nthreads > NTHREADS_MAX:
        if nthreads < NTHREADS_MIN or nthreads > (NTHREADS_MAX - NUM_TEAMS + 1):
            valid = False
            break
    if valid:
        #total = int(sum(params))
        #print("SUM = {}".format(total))
        valid = True if sum(params) <= NTHREADS_MAX else False
    
    return valid
