# pram
Python implementation of post-randomisation method for disclosure control

## Usage

Call the pram() method with a Pandas dataframe to apply post-randomisation perturbation
to the dataset using a generated transition matrix.

You can specify the minimum diagonal value (i.e. the minimum probability
that a data point remains unchanged) and an alpha value to modify the
likelihood of perturbation (from zero to one). 

The behaviour is largely the same as that in the "sdcMicro" R package.

## Command-line usage

You can also call Pram from the command line, supplying a CSV file
input and path to output the perturbed dataset as CSV.

## Example

~~~
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
print(Pram.pram(df))
~~~