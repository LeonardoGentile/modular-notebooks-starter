from os import read
from pandas.core.frame import DataFrame
from pandas.io.sql import DatabaseError
from lib.constants import DATA_DIR_PATH, DATA_FILE_NAME, READ, WRITE, CSV, XLS
from typing import Union
from pathlib import Path

import pandas as pd


# FILE HANDLING
# ======================

# DATA LOADING AND SAVING
def _get_file_path(data_dir_path: Union[str, Path] = DATA_DIR_PATH,
                   data_file_name: str = None,
                   data_file_path: Path = None) -> Path:
    """Given a data data_dir_path+data_file_name or a data_file_path return the abs path of the data file

    Args:
        data_dir_path (Union[str, Path], optional): Dir where csv|xls main files are stored. Defaults to DATA_DIR_PATH
        file_name (str, optional): Main Data File Name. Defaults to None.
        file_path (Path, optional): Absolute path to data file, if passed has the priority. Defaults to None.

    Returns:
        Path: Absolute path location
    """
    ret_path = None
    if data_file_path:
        ret_path = data_file_path
    else:
        ret_path = Path(data_dir_path).joinpath(data_file_name)
    return ret_path


def _load_or_dump_df(data_dir_path: Union[str, Path] = DATA_DIR_PATH,
                     data_file_name: str = None,
                     data_file_path: Union[Path, None] = None,
                     file_type: str = CSV,
                     operation: str = READ,
                     df: Union[None, pd.DataFrame] = None,
                     **kwargs) -> Union[None, pd.DataFrame]:
    """Load or save a csv|xls from/to a file and return a df/None

    First compute the absolute path of the file then load it into a pd and return itself.
    The path is computed either by dir_path + file_name or by passing the abs data_file_path.

    Args:
        data_dir_path (Union[str, Path], optional): Dir where csv|xls main files are stored. Defaults to DATA_DIR_PATH
        file_name (str, optional): Main Data File Name. Defaults to None.
        file_path (Path, optional): Absolute path to data file, if passed has the priority. Defaults to None.
        file_type (str, optional): 'csv' or 'xls'. Defaults to 'csv'.
        operation (str, optional): IO Operation (READ/WRITE) type Defaults to READ
        df (pd.Dataframe, optional): In case of write operation it is necessary to pass the df to dump
        **kwargs (Dict, optional): pass any addition **kwargs to the pd function used for reading the file (read_excel, read_csv)

    Returns:
        pd.DataFrame: [description]
    """
    data_file_path = _get_file_path(data_dir_path,
                                    data_file_name,
                                    data_file_path)
    map_fn = {
        CSV: {
            READ: pd.read_csv,
            WRITE: getattr(df, 'to_csv', None)
        },
        # it requires the proper libraries to read excel files
        XLS: {
            READ: pd.read_excel,
            WRITE: getattr(df, 'to_excel', None)
        }
    }

    fn = map_fn[file_type][operation]
    df = fn(data_file_path, **kwargs)
    return df


def load_df(data_dir_path: Union[str, Path] = DATA_DIR_PATH,
            data_file_name: str = DATA_FILE_NAME,
            data_file_path: Union[Path, None] = None,
            file_type: str = CSV, **kwargs) -> pd.DataFrame:
    """Load a csv|xls file and return a df"""
    return _load_or_dump_df(data_dir_path, data_file_name,
                            data_file_path, file_type,
                            operation=READ, **kwargs)


def dump_df(df: pd.DataFrame,
            data_dir_path: Union[str, Path] = DATA_DIR_PATH,
            data_file_name: str = None, data_file_path: Union[Path, None] = None,
            file_type: str = CSV, **kwargs) -> None:
    """save a csv|xls to file"""
    return _load_or_dump_df(data_dir_path, data_file_name,
                            data_file_path, file_type,
                            operation=WRITE, df=df, **kwargs)


# FIND / DROP Conditions
# ======================
def find_cols_by_row_condition(df: pd.DataFrame, filt) -> pd.Series:
    """Return an Array of column indices

        Accepts filt row conditions like:
            dframe.iloc[0] == 'ML_DAY'
            dframe.loc['col_name'].isin([np.NaN, 0])
    """
    df_filt = df.loc[:, filt]  # dataframe with filtered columns
    cols = df_filt.columns  # Array of the filtered column indices
    return cols


def drop_rows_by_col_condition(df: pd.DataFrame, filt) -> pd. DataFrame:
    """Drop rows by a condition on column(s). Return the filtered df

        Accepts filt conditions like:
            df['ML_DAY'] == 0
    """
    df = df.drop(df.loc[(filt), :].index, axis=0)
    return df


def get_slider(col1: str, col2: str) -> slice:
    # Example: how to save a slicer into a variable
    cols_slicer = slice(col1, col2, None)
    return cols_slicer


# NA/Null Values
# ==============
# TODO:rename get_na_cols_ratio
def get_na_cols(df: pd.DataFrame, tresh=0, as_percentage=False, asc=False) -> pd.Series:
    """Return the ratio of how many rows are null by column

    Return the ration as [0-1] ratio or as percentage
    Optionally shows only columns having NA > tresh [0-1]
    """
    # Equivalent but Unclean version: na_cols = (df.isnull().sum() / df.shape[0]) * 100
    na_cols = df.isnull().mean()
    na_cols = na_cols[na_cols > tresh].sort_values(ascending=asc)
    if as_percentage is True:
        na_cols *= 100
    return na_cols


def print_na_cols(df: pd.DataFrame, tresh=0, asc=False, df_name='') -> None:
    """Give a df print stats on how many null values by column"""
    na_cols = get_na_cols(df, tresh=tresh, as_percentage=True, asc=asc)
    print("\n% of missing values in the {} data set by column:".format(df_name))
    print("\n".join("{:>20.20} {:5.2f}%".format(name, value)
          for name, value in na_cols.iteritems())
          )

# TODO: Rename perc -> tresh


def drop_na_cols(df: pd.DataFrame, perc: float = 0.5) -> pd.DataFrame:
    """ Drop columns whose % of NA is > perc [0-1]

       If perc not specified, than assume 50%
    """
    return df.dropna(axis=1, thresh=int(perc*len(df)))


def drop_duplicate_cols(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicated colulms from a df

    # https://stackoverflow.com/questions/14984119/python-pandas-remove-duplicate-columns/40435354#40435354

    Args:
        df (pd.DataFrame): df with duplicated column names

    Returns:
        pd.DataFrame: df without
    """

    df = df.loc[:, ~df.columns.duplicated()]
    return df


def get_all_na_rows(df: pd.DataFrame) -> pd.DataFrame:
    return df[df.isna().all(axis=1)]


# CONVERSION
# ==========
def index_to_datetime(df: pd. DataFrame) -> pd.DataFrame:
    df_dt = df.copy()
    df_dt.index = pd.to_datetime(df_dt.index)
    return df_dt


# To verify the type
# df_info.applymap(type)
# df.applymap(type)
