# Intrusion-Tolerance as a Service (ITaaS) Optimizer

## Creator: Maher Khan
## Advisor: Amy Babay

Welcome to the ITaaS Optimizer GitHub repository! This project focuses on evaluating the efficacy and scalability of our Intrusion-Tolerance as a Service (ITaaS) through a series of experiments across different service models (SM1, SM2, and SM3).

## Experimental Setup

### Synthetic Application Data and Available Resources

To comprehensively assess performance, we generate synthetic application data, varying application set sizes and fault tolerance characteristics. This ensures diverse datasets reflecting real-world scenarios. Additionally, we define a fixed set of resources distributed across various geographic locations, facilitating meaningful comparisons across different algorithms and service models.

<!-- For detailed experimental setup information, refer to [Experimental Setup Details](#experimental-setup-details). -->

## ITaaS Components

### ITaaS Optimizer

Our ITaaS Optimizer systematically runs heuristic algorithms and MILP formulations for each service model on application sets and available resources. The output is a list of placements, indicating where each replica should be hosted.

### ITaaS Validator

The ITaaS Validator ensures resultant placements meet requirements for each service model. It checks various conditions including site existence, replica counts, latency constraints, and more. It is run on the list of placements, which is the output of the optimizer.

### ITaaS Quality Calculator

The Quality Calculator measures placement quality through quantitative metrics like the number of applications assigned, replicas used, and physical servers utilized. It enables structured analysis and comparison across different scenarios. It is run on the list of placements, which is the output of the optimizer.

## ITaaS Evaluator

Our evaluation tool compares heuristic algorithms against optimal MILP solutions across all service models. Key metrics such as violations, applications assigned, replicas/machines used, and execution time are analyzed, providing insights into efficacy, scalability, and trade-offs.

<!-- For more detailed information, refer to our [Experimental Setup Details](#experimental-setup-details). -->

<!-- ## Experimental Setup Details

For a comprehensive understanding of our experimental setup, including synthetic application data generation and resource distribution, refer to [Experimental Setup Details](#experimental-setup-details) in the documentation. -->

## Getting Started

### Generating Synthetic Application Data

To generate synthetic application data, run the following command:

```bash
python3 ITaaS_Synthetic_Apps_Generator.py
```

### Running Optimizers for Service Model 1

To run heuristic and Mixed-Integer Linear Programming (MILP) optimizers for Service Model 1 on synthetic data, use the following commands:

```bash
python3 ITaaS_SM1_Heuristic_Optimizer.py
python3 ITaaS_SM1_MILP_Optimizer.py
```

### Running Optimizers for Service Model 2

To run heuristic and Mixed-Integer Linear Programming (MILP) optimizers for Service Model 2 on synthetic data, use the following commands:

```bash
python3 ITaaS_SM2_Heuristic_Optimizer.py
python3 ITaaS_SM2_MILP_Optimizer.py
```

### Running Optimizers for Service Model 3

To run heuristic and Mixed-Integer Linear Programming (MILP) optimizers for Service Model 3 on synthetic data, use the following commands:

```bash
python3 ITaaS_SM3_Heuristic_Optimizer.py
python3 ITaaS_SM3_MILP_Optimizer.py
```

### Evaluating Benchmark Results

To evaluate benchmark results for all three service models and create comparison graphs, run the following command:

```bash
python3 ITaaS_Evaluator.py
```

## Speeding Up Optimizers

For faster execution of the optimizers, it's recommended to use PyPy3 instead of Python3. PyPy3 is an alternative Python interpreter that often provides significant performance improvements, especially for compute-intensive tasks like optimization algorithms.

To install PyPy3, visit the [PyPy website](https://www.pypy.org/) and follow the installation instructions for your operating system.

Once PyPy3 is installed, you can use it to run the optimizers by replacing `python3` with `pypy3` in the command line. For example:

```bash
pypy3 ITaaS_SM1_Heuristic_Optimizer.py
pypy3 ITaaS_SM1_MILP_Optimizer.py
```

Note that pypy3 currently does not work with ITaaS_Evaluator.py since this program uses some libraries not yet supported by pypy3

## Private License

License terms and conditions detailed in License.txt available in the source code repository.
