# Lattice Structure Computation Program

This generates lattice structures from unit lattice meshes (.msh or ANSYS ASCII nodes + elements in .txt format)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
python 3.6
pip install numpy
pip install progressbar2
GMSH installed and added to PATH
```

### Installing

Run Lattice Generation by running in the project directory:

```
python app.py
```

Output files are placed in lattice\output in .stl and .msh format

## Running the tests

Go to the directory and run:

```
python unit_test.py
```

To test different values, change the *x,y,z* values in `individual_test()`. 

To run a general set of unit tests,  replace `individual_test(...)` with `unitTest(nodes, elements, displacement_factor)`.

All test outputs are written in `output\test_output.txt`

## Authors

* **Timothy Lu** - [timothylu](https://github.com/timothylu)
* **Antony Hwang** - [AntonyHwang](https://github.com/AntonyHwang)
