# Lattice Structure Computation Program

This generates lattice structures from unit lattice meshes (.msh or ANSYS ASCII nodes + elements in .txt format)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them


* [python 3.6](https://www.python.org/downloads/)
* [numpy](http://www.numpy.org/)
* [progressbar2](https://pypi.python.org/pypi/progressbar2)
* [GMSH](http://gmsh.info/)


GMSH can be installed from the link [here](http://gmsh.info/#Download). After you extract it, the direcctory must be added to the path.

Numpy and Progressbar can be installed by calling:
```
pip install numpy
pip install progressbar2
```
in the command-line.

### Generating a Lattice

Run Lattice Generation by running in the project directory:

```
python app.py
```

input the model you want to multiply `45` or `90`, followed by the dimensions of the volume `x,y,z`.

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
