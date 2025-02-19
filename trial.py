import subprocess
import time
from deap import benchmarks
from nbody_runner import NBodyRunner

NTHREADS_MIN = 40
NTHREADS_MAX = 120
NTHREADS_TOTAL = 240
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
run_script = 'run_dubinsky.sh' # Obsolete, see the init method of nbody runner
build_script = 'build_dubinsky.sh'
cleanup_script = 'cleanup_dubinsky.sh'
# Timestep parameter of the nbody program
nbody_timestep = 0.00001
# Timeout in sec, set to None for unlimited
run_timeout = 60

n_trial = 0
retry = 3

def run(params):
    #print("[Trial] {}".format(params))
    #return benchmarks.ackley(params)
    #return exec_benchmark(params)
    global n_trial
    n_trial += 1
    if (n_trial % 100) == 0:
        time.sleep(3)

    print("[Trial-{}] {}".format(n_trial, params))
    return exec_nbody_py3(params),

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

def exec_nbody_py3(params):
    nbody_runner = NBodyRunner(nbody_workdir, NUM_TEAMS, src_filename, temp_src_filename,\
                               run_script, build_script, cleanup_script, timestep=nbody_timestep)
    #exec_times = nbody_runner.execute_nbody_alt(params, run_timeout)
    #exec_times = nbody_runner.execute_nbody_check(params, run_timeout)
    #exec_times = nbody_runner.execute_nbody_check_output(params, run_timeout)
    exec_times = nbody_runner.execute_nbody_monitor(params, run_timeout)
    result = exec_times[1]
    
    # Retry mechanism if there is something fishy with the execution
    n = 0
    while result == None and n < retry:
        print("** Restarting ({})..".format(n+1))
        time.sleep(2)
        #exec_times = nbody_runner.execute_nbody_alt(params, run_timeout)
        exec_times = nbody_runner.execute_nbody_monitor(params, run_timeout)
        result = exec_times[1]
        n += 1

    # If it still fails, set the weights to the penalty value, s.t. the optimizer can continue
    if result == None:
        result = INVALID_NTHREADS_PENALTY
        print("[WARN] The execution has failed, this candidate will be considered unfeasible.")

    return result
    
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
        if nthreads < NTHREADS_MIN or nthreads > NTHREADS_MAX:
            valid = False
            break
    if valid:
        #total = int(sum(params))
        #print("SUM = {}".format(total))
        valid = True if sum(params) <= NTHREADS_TOTAL else False
    
    return valid
