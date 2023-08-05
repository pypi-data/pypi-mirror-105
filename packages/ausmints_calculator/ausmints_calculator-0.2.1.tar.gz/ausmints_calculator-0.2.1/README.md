# Calculator

This calculator is a library than can be used for simple arithmetic operations.
A calculator object should be created from the Calculator class defined inside the module. The object will have a "memory" attribute which will be operated upon and returned by the Calculator methods.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install ausmints_calculator.

```bash
pip install ausmints_calculator
```

## Usage

```python
from ausmints_calculator import Calculator

calc = Calculator()

calc.memory # returns 0
calc.add(5) # returns 5
calc.squared() # returns 25
calc.reset_memory() # returns 0
```

For more extensive examples see the [test](https://github.com/TuringCollegeSubmissions/jausmi-DT.1.1/blob/master/tests/test_calculator.py) file

## Docker
A Dockerfile is added that can be used to create python 3.8 environment with the calculator module already installed

## Roadmap
- A functionality that saves and remembers the "memory" variable between sessions could be created.
- Functionality that allows the user to save various results into a different memory variable (maybe a dict type). These values could be later accessed and set as active.

## [Changelog](https://github.com/TuringCollegeSubmissions/jausmi-DT.1.1/blob/master/CHANGELOG.md)


## License
[MIT](https://choosealicense.com/licenses/mit/)