# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Setup Notebook: Import, Cleanup, Normalize & Split Data

# %% [markdown]
# ### Lib imports & Options

# %%
import sys
from typing import Dict, OrderedDict, Tuple
import warnings
from collections import namedtuple

# ML libs
import numpy as np
import pandas as pd

# ASSERTS
# Python ≥3.5 is required
assert sys.version_info >= (3, 5)

# Pandas options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 25)


# Ignore useless warnings (see SciPy issue #5998)
warnings.filterwarnings(action="ignore", message="^internal gelsd")


# %% [markdown]
# ### Import my libs

# %% [markdown]
# - The `loader` module is a py module located in the same dir of the notebooks.
# It sets up the `PYTHONPATH` in order to import py modules from other dirs within the project root.
# This way you can import the generated scripts (in `/src`) from within a notebook.
# - The `reloader` module let you reload the imported py modules (deep reload) that were modified since last time they were imported.
# By calling `reloader.clear()` it invalidated the cache of imported modules that were modified.

# %%
import loader # set PYTHONPATH for imports
import reloader # Reload local modified files with


# %% [markdown]
# Verify that the syspath was indeed modified by the `loader`. 
# You should see a list of path here where python module are looked up, the last one should be your project root.

# %%
print(sys.path)

# %% [markdown]
# Once `import loader` has been executed you can now import other modules located in different directories under your project root.

# %%
from lib.pd import load_df, drop_na_cols, print_na_cols


# %% [markdown]
# If any of your external modules was modified then execute this cell but don't forget to comment it again once reloaded the modules or it will created import troubles when this notebook will be imported as module.

# %%
# reloader.clear() # ⚠️ Uncomment and execute this to reload modules that were modified


# %% [markdown]
# ## Load the Data & Arrange the data structure

# %% [markdown]
# `load_df` with no arguments takes the `data_file_abs_path` OR `data_dir` + `data_file_name` defined in `config.toml`

# %%
df = load_df() 
df

# %%
print_na_cols(df)

# %% [markdown]
# Example of imported function from the `lib` dir

# %%
# Drop all columns having more than 60% of missing values
df = drop_na_cols(df, perc=0.6)
df.head() # Content and Headquarters were dropped

# %% [markdown]
# we can pass multiple arguments to `load_df`, they will combine with what's defined in `config.toml`

# %%
df_future50 = load_df(data_file_name='Future50.csv')
df_future50.head()

# %%
print_na_cols(df_future50)


# %% [markdown]
# ## Other data Manipulation
#
# Usually you need to cleanup and re-arrange the data structure 

# %% [markdown]
# ## Exported Vars
#
# Since we want to import this notebooks as if it was (it will be) a python module from another notebook, it would be nice not to pollute that notebooks with all the variables of this one.   
# A solution would be to have a function to return only the needed variables, for example:

# %%
def get_export():
    return df, df_future50

# %% [markdown]
# So we can simply import `from src.load_data import get_export` and get the vars by executing `get_export`

# %% [markdown]
# # Transform this notebook into a python module
#
# Automatically whenever you save this notebook then **Jupytext** will export a new script in `src/load_data.py`

# %%
