import pytest
import pandas as pd
from app import flatten  # Assuming your function is in app.py

def test_flatten_with_no_nesting():
    """Test case for a dataframe with no nested columns."""
    data = {
        'A': [1, 2, 3],
        'B': ['X', 'Y', 'Z']
    }
    df = pd.DataFrame(data)
    flattened_df = flatten(df)
    
    # Check that the dataframe remains the same
    pd.testing.assert_frame_equal(df, flattened_df)

def test_flatten_with_list_in_column():
    """Test case for a dataframe with lists in a column."""
    data = {
        'A': [1, 2, 3],
        'B': [['X', 'Y'], ['Z'], ['W', 'X']]
    }
    df = pd.DataFrame(data)
    flattened_df = flatten(df)
    
    # Check that the 'B' column was exploded correctly
    expected_data = {
        'A': [1, 1, 2, 3, 3],
        'B': ['X', 'Y', 'Z', 'W', 'X']
    }
    expected_df = pd.DataFrame(expected_data)
    
    pd.testing.assert_frame_equal(flattened_df, expected_df)

def test_flatten_with_dict_in_column():
    """Test case for a dataframe with dictionaries in a column."""
    data = {
        'A': [1, 2, 3],
        'B': [{'key1': 'value1', 'key2': 'value2'}, {'key1': 'value3', 'key2': 'value4'}, {'key1': 'value5', 'key2': 'value6'}]
    }
    df = pd.DataFrame(data)
    flattened_df = flatten(df)
    
    # Check that the dictionary in column 'B' is normalized and flattened
    expected_data = {
        'A': [1, 2, 3],
        'B_key1': ['value1', 'value3', 'value5'],
        'B_key2': ['value2', 'value4', 'value6']
    }
    expected_df = pd.DataFrame(expected_data)
    
    pd.testing.assert_frame_equal(flattened_df, expected_df)

def test_flatten_with_multiple_nested_columns():
    """Test case for a dataframe with both lists and dictionaries in different columns."""
    data = {
        'A': [1, 2],
        'B': [{'key1': 'value1'}, {'key1': 'value2'}],
        'C': [['X', 'Y'], ['Z']]
    }
    df = pd.DataFrame(data)
    flattened_df = flatten(df)
    
    # Check that both 'B' and 'C' columns are flattened correctly
    expected_data = {
        'A': [1, 2, 1, 2],
        'B_key1': ['value1', 'value2', 'value1', 'value2'],
        'C': ['X', 'Y', 'Z', 'Z']
    }
    expected_df = pd.DataFrame(expected_data)
    
    pd.testing.assert_frame_equal(flattened_df, expected_df)

def test_flatten_with_empty_column():
    """Test case for a dataframe with an empty column (no data)."""
    data = {
        'A': [1, 2, 3],
        'B': [[], [], []]
    }
    df = pd.DataFrame(data)
    flattened_df = flatten(df)
    
    # Check that the 'B' column remains unchanged, but exploded (empty lists)
    expected_data = {
        'A': [1, 2, 3],
        'B': [None, None, None]  # Exploding empty lists results in NaN/None
    }
    expected_df = pd.DataFrame(expected_data)
    
    pd.testing.assert_frame_equal(flattened_df, expected_df)

if __name__ == '__main__':
    pytest.main()
