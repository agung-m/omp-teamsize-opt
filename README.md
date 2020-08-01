# omp-teamsize-opt
A collection of tools for automatic tuning of OMP thread team size.

With some modifications, these tools can also be used for other tuning of runtime parameters.
Generic implementations are planned as future work.

### Current implementations:
1. Differential Evolution (DE, an evolutionary-based algorithm)

### Usage
An example of tuning the NBody program using DE:

1. Clone the teamsize-opt project from github, place the teamsize-opt directory to the parent directory of your program, e.g., one level above src/
2. Create a script to change the parameters and run the program:
  - See trial.py, run_dubinsky.sh and Makefile-parallel for examples
3. Run the optimizer rom the parent directory:

   <code>$ python teamsize-opt/teamsize_de_opt.py</code>
