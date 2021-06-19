import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer


def fill_na_mean(df: pd.DataFrame) -> pd.DataFrame:
    """Get a df and return it filled with mean values (by col) instead of NA

    The imputer simply computes the mean (or another strategy we chose)
    of each attribute and stores the result in its statistics_ instance variable.

    Args:
        df (pd.DataFrame): dataframe

    Returns:
        pd.DataFrame: dataframe
    """

    """SimpleImputer Usage:
        A) Two steps
        - imputer_mean.fit(df) then
        - imputer_mean.transform(df)
        It stores the computed values into:
            `imputer_mean.statistics_`
            Equivalent to `df.mean().values`

        B) Or a single step:
        - imputer_mean.fit_transform(df)
        The result is an np.ndarray to be transformed back into pandas df
    """
    imputer_mean = SimpleImputer(missing_values=np.nan, strategy='mean')
    # plain NumPy array containing the transformed feature
    np_arr = imputer_mean.fit_transform(df)
    df = pd.DataFrame(np_arr, columns=df.columns, index=df.index)
    return df
