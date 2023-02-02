**Link Budget Analysis**

## About the tool
This analysis tool is developed to carry out link budget analysis. 

## Organization
cfg directory consists of configuration files for input parameters. Change the configuration files or create new ones to analyze the link.
src directory consists of the parsing of the configration iles, and other executables.

## Instructions
1. To get started, first clone this repo:
```
git clone <repo link>
cd <directory>
```
2. Install all the requirements:
Starting from the repository root, open a terminal. Execute:
```
cd link_budget_analysis
pip install -e .
```
*If this does not work, try 1) updating pip, 2) updating setuptools

3. You can run the code by executing the following file:

src/link_budget_analysis/link_analysis.py


## Upcoming improvements:
1. implementing venv [resouces here](https://docs.python.org/3/library/venv.html)
2. improving the link_analysis variables input - make it less jank
2. implementing `analysis_type: "configuration"` which would lead to plot the link margin with data rate vs length