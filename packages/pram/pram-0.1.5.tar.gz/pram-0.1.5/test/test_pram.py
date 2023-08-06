from pram import Pram, pram
import numpy as np
import pandas as pd


def test_get_transition_matrix_equal():
    data = ['Male', 'Female', 'Male', 'Female']
    matrix = Pram.__get_transition_matrix__(data)
    assert(((matrix.values[0] == 0.5) & (matrix.values[1] == 0.5)).all())


def test_get_transition_matrix_majority():
    data = ['Male', 'Male', 'Male', 'Female']
    matrix = Pram.__get_transition_matrix__(data)
    assert(((matrix.values[0] == 0.25) & (matrix.values[1] == 0.75)).all())


def test_get_transition_matrix_same():
    data = ['Male', 'Male', 'Male', 'Male']
    matrix = Pram.__get_transition_matrix__(data)
    assert((matrix.values[0] == 1).all())


def test_get_weighted_transition_matrix_equal():
    data = ['Male', 'Female', 'Male', 'Female']
    matrix = Pram.__get_weighted_transition_matrix__(data, 0.8, 0.5)
    assert_matrix_is_valid(matrix)
    assert(matrix.values[0, 0] + matrix.values[1, 1] >= 1.6)
    assert (matrix.values[0, 1] + matrix.values[1, 0] <= 0.4)
    assert (matrix.values[0, 0] == matrix.values[1, 1])
    assert (matrix.values[0, 1] == matrix.values[1, 0])


def test_get_weighted_transition_matrix_majority():
    data = ['Male', 'Female', 'Male', 'Male']
    matrix = Pram.__get_weighted_transition_matrix__(data, 0.8, 0.5)
    assert_matrix_is_valid(matrix)
    assert(matrix.values[0, 0] < matrix.values[1, 1])
    assert(matrix.values[0, 1] < matrix.values[1, 0])


def test_get_weighted_transition_matrix_majority_opposite():
    data = ['Male', 'Female', 'Female', 'Female']
    matrix = Pram.__get_weighted_transition_matrix__(data, 0.8, 0.5)
    assert_matrix_is_valid(matrix)
    assert(matrix.values[0, 0] > matrix.values[1, 1])
    assert(matrix.values[0, 1] > matrix.values[1, 0])


def test_get_weighted_transition_matrix_majority_no_mods():
    data = ['Male', 'Male', 'Male', 'Female']
    matrix = Pram.__get_weighted_transition_matrix__(data, 0.0, 1.0)
    assert_matrix_is_valid(matrix)
    assert(matrix.values[0, 0] < matrix.values[1, 1])
    assert(matrix.values[0, 1] < matrix.values[1, 0])
    assert (matrix.values[0, 0] == 0.25)
    assert (matrix.values[1, 1] == 0.75)


def test_get_weighted_transition_matrix_majority_identity():
    data = ['Male', 'Male', 'Male', 'Female']
    matrix = Pram.__get_weighted_transition_matrix__(data, 0.0, 0)
    assert_matrix_is_valid(matrix)
    assert(matrix.values[0, 0] == matrix.values[1, 1])
    assert(matrix.values[0, 1] == matrix.values[1, 0])
    assert (matrix.values[0, 0] == 1)
    assert (matrix.values[1, 1] == 1)


def test_get_weighted_transition_matrix_majority_50_alpha():
    data = ['Male', 'Male', 'Male', 'Female']
    matrix = Pram.__get_weighted_transition_matrix__(data, 0.0, 0.5)
    assert_matrix_is_valid(matrix)
    assert(matrix.values[0, 0] < matrix.values[1, 1])
    assert(matrix.values[0, 1] < matrix.values[1, 0])
    assert (matrix.values[0, 0] == 0.625)
    assert (matrix.values[1, 1] == 0.875)


def test_replace_identity():
    data = ['Male', 'Male', 'Male', 'Female']
    matrix = Pram.__get_weighted_transition_matrix__(data, 0.0, 0)
    values = ['Male', 'Male', 'Male', 'Male']
    new_values = []
    for value in values:
        new_values.append(Pram.__pram_replace__(matrix, value))
    assert(new_values == values)


def test_replace_majority_unweighted():
    np.random.seed(1234)
    data = ['Male', 'Male', 'Male', 'Female']
    matrix = Pram.__get_weighted_transition_matrix__(data, 0.0, 1.0)
    values = ['Female', 'Female', 'Female', 'Female', 'Female', 'Female', 'Female', 'Female', 'Female', 'Female']
    new_values = []
    for value in values:
        new_values.append(Pram.__pram_replace__(matrix, value))
    assert(new_values == ['Female', 'Male', 'Male', 'Male', 'Male', 'Male', 'Male', 'Male', 'Male', 'Male'])


def test_replace_majority_weighted():
    np.random.seed(1234)
    data = ['Male', 'Male', 'Male', 'Female']
    matrix = Pram.__get_weighted_transition_matrix__(data, 0.8, 0.5)
    values = ['Female', 'Female', 'Female', 'Female', 'Female', 'Female', 'Female', 'Female', 'Female', 'Female']
    new_values = []
    for value in values:
        new_values.append(Pram.__pram_replace__(matrix, value))
    assert(new_values == ['Female', 'Female', 'Female', 'Male', 'Male', 'Female', 'Female', 'Male', 'Male', 'Male'])


def test_stratification():
    np.random.seed(1000)
    data = [
        {'gender': 'male', 'education': 'low'},
        {'gender': 'male', 'education': 'low'},
        {'gender': 'male', 'education': 'low'},
        {'gender': 'male', 'education': 'low'},
        {'gender': 'male', 'education': 'high'},
        {'gender': 'female', 'education': 'low'},
        {'gender': 'female', 'education': 'high'},
        {'gender': 'female', 'education': 'high'},
        {'gender': 'female', 'education': 'high'},
        {'gender': 'female', 'education': 'high'}
    ]
    df = pd.DataFrame(data)

    out = pram(df, m=0.0, alpha=1.0, strata='gender')

    male = out[(df.gender == 'male')].values.__len__()
    female = out[(df.gender == 'female')].values.__len__()
    high_education_male = out[(df.gender == 'male') & (df.education == 'high')].values.__len__()
    high_education_female = out[(df.gender == 'female') & (df.education == 'high')].values.__len__()

    # Education changes in line with the proportions stratified by gender - so the
    # end proportions are the same but the actual rows are not.
    assert(not out.equals(df))
    assert(high_education_male == 1)
    assert(high_education_female == 4)
    # None of the genders should change
    assert(male == 5)
    assert(female == 5)


def assert_matrix_is_valid(matrix):
    """
    Check that a matrix sums to 1 in each column
    :param matrix: the matrix to test
    :return: None
    """
    assert(matrix.values[0, 0] + matrix.values[1, 0] == 1)
    assert(matrix.values[0, 1] + matrix.values[1, 1] == 1)