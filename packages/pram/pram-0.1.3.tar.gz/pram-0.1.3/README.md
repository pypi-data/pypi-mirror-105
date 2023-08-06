# pram
Python implementation of post-randomisation method for disclosure control

[![Build Status](https://travis-ci.com/scottbw/pram.svg?branch=main)](https://travis-ci.com/scottbw/pram)
[![License](https://img.shields.io/pypi/l/pram.svg?branch=main)](https://github.com/scottbw/pram/blob/main/LICENSE)
[![Status](https://img.shields.io/pypi/status/pram.svg?branch=main)](https://pypi.org/project/pram/)
[![Supported versions](https://img.shields.io/pypi/pyversions/pram.svg?branch=main)](https://pypi.org/project/pram/)
[![Version](https://img.shields.io/pypi/v/pram.svg?branch=main)](https://pypi.org/project/pram/)

Call the pram() method with a Pandas dataframe to apply post-randomisation perturbation
to the dataset using a generated transition matrix.

You can specify the minimum diagonal value (i.e. the minimum probability
that a data point remains unchanged) and an alpha value to modify the
likelihood of perturbation (from zero to one). 

By default all columns are modified, and there is no stratification. However
you can specify the columns to process as a list, and also specify
a column to use for stratification. If stratification is used, the
column used for stratification is not modified.

The behaviour is largely the same as that in the "sdcMicro" R package.

## Command-line usage

You can also call Pram from the command line, supplying a CSV file
input and path to output the perturbed dataset as CSV.

From the command line you can also use the -f switch to print a 
table of the frequencies of categories in the original and changed
versions of the dataset.

Example: 

`pram mydata.csv output.csv 0.8 0.5 -f`

This will load the data in mydata.csv, run PRAM with m=0.8 and a=0.5, save
the output in output.csv, and print a frequency table to the console.

## Example

~~~
from pram import pram
persons = [
{'gender': 'female', 'region': 'rural', 'education': 'higher', 'age': 27},
{'gender': 'female', 'region': 'rural', 'education': 'lower', 'age': 35},
{'gender': 'male', 'region': 'rural', 'education': 'lower', 'age': 26},
{'gender': 'male', 'region': 'rural', 'education': 'lower', 'age': 22},
{'gender': 'female', 'region': 'urban', 'education': 'higher', 'age': 41},
{'gender': 'female', 'region': 'urban', 'education': 'lower', 'age': 54},
{'gender': 'female', 'region': 'rural', 'education': 'higher', 'age': 38},
{'gender': 'female', 'region': 'rural', 'education': 'lower', 'age': 44},
{'gender': 'male', 'region': 'rural', 'education': 'lower', 'age': 18},
{'gender': 'male', 'region': 'rural', 'education': 'lower', 'age': 52},
{'gender': 'female', 'region': 'urban', 'education': 'higher', 'age': 44},
{'gender': 'female', 'region': 'urban', 'education': 'lower', 'age': 35},
{'gender': 'female', 'region': 'rural', 'education': 'higher', 'age': 33},
{'gender': 'female', 'region': 'rural', 'education': 'lower', 'age': 31},
{'gender': 'male', 'region': 'rural', 'education': 'lower', 'age': 40},
{'gender': 'male', 'region': 'rural', 'education': 'lower', 'age': 23},
{'gender': 'female', 'region': 'urban', 'education': 'higher', 'age': 68},
{'gender': 'female', 'region': 'urban', 'education': 'lower', 'age': 19},
{'gender': 'female', 'region': 'rural', 'education': 'higher', 'age': 27},
{'gender': 'female', 'region': 'rural', 'education': 'lower', 'age': 24},
{'gender': 'male', 'region': 'rural', 'education': 'lower', 'age': 48},
{'gender': 'male', 'region': 'rural', 'education': 'lower', 'age': 38},
{'gender': 'female', 'region': 'urban', 'education': 'higher', 'age': 30},
{'gender': 'female', 'region': 'urban', 'education': 'lower', 'age': 27}
]
df = pd.DataFrame(persons)
print(pram(df))
~~~