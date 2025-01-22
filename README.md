# OpenMP Thread Team Size Optimizer
*omp-teamsize-opt* is a package for automatically tuning OpenMP (OMP) thread team size.

## Features
- AI-based optimization, currently using [Differential Evolution (DE)](https://en.wikipedia.org/wiki/Differential_evolution)
- Faster than grid-search, better than random-search 
- Extensible; optimizer is decoupled from the target application

## Extensibility
With minimal modifications, the optimizer can also be used to tune applications with [hyperparameters](https://en.wikipedia.org/wiki/Hyperparameter_optimization).

A generic implementation is planned as future work. Everyone is welcome to contribute.

## Cite this work
Please see the following papers for details and to cite this work:

Xiao, X., Agung, M., Amrizal, M.A., Egawa, R. and Takizawa, H., 2018, November. Investigating the Effects of Dynamic Thread Team Size Adjustment for Irregular Applications. In 2018 Sixth International Symposium on Computing and Networking (CANDAR) (pp. 76-84). IEEE. https://doi.org/10.1109/CANDAR.2018.00017


## Usage
An example of tuning the NBody program:

1. Clone omp-teamsize-opt, place the omp-teamsize-opt directory to the parent directory of the target program, e.g., one level above src/
2. Create script(s) to change the parameters and run the program. See [trial.py](/trial.py) and [run_dubinsky.sh](/run_dubinsky.sh) for examples
4. Run the optimizer from the parent directory:
   
   `python teamsize_de_opt.py`

## License
Apache License 2.0

## Contributions
The current maintainer is [agung-m](https://github.com/agung-m)


