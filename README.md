# OpenMP Thread Team Size Optimizer
*omp-teamsize-opt* is a tool for automatically tuning OpenMP (OMP) thread team size.

## Features
- AI-based optimization, currently using [Differential Evolution (DE)](https://en.wikipedia.org/wiki/Differential_evolution)
- Faster than grid-search due to fewer tests 
- Extensible; optimizer is decoupled from the target application

## Extensibility
With some modifications, the optimizer can also be used for tuning other runtime parameters and [hyperparameters](https://en.wikipedia.org/wiki/Hyperparameter_optimization).

A generic implementation is planned as future work. Everyone is welcome to contribute.

## Cite this work
Please see the following publication for details and to cite this work.

Xiao, X., Agung, M., Amrizal, M.A., Egawa, R. and Takizawa, H., 2018, November. Investigating the Effects of Dynamic Thread Team Size Adjustment for Irregular Applications. In 2018 Sixth International Symposium on Computing and Networking (CANDAR) (pp. 76-84). IEEE. https://doi.org/10.1109/CANDAR.2018.00017


## Usage
opt-teamsize-opt needs Python and the [DEAP package](https://deap.readthedocs.io/en/master/installation.html) installed. See [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html) to quickly install Python and packages.

An example of tuning the NBody program:

1. Download the project code:  
   `git clone https://github.com/agung-m/omp-teamsize-opt.git`
2. Create a script to run the program with different parameters. See [nbody_runner.py](/nbody_runner.py) and [trial.py](/trial.py).
3. Run the optimizer:  
   `python teamsize_de_opt.py`

## License
Apache License 2.0

## Contributions
The current maintainer is [agung-m](https://github.com/agung-m)


