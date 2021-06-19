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
# # Correlation Notebook

# %% [markdown]
# ### Imports

# %%
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

import loader
import reloader

# %%
from lib.helpers import suppress_stdout
from lib.pd import dump_df
from lib.plt import save_fig

# %%
# reloader.clear()

# %% [markdown]
# ### Import a notebook a python module

# %% [markdown]
# Import my notebooks as a python module!
# Now I can decide exactly what I want to import from it

# %%
with suppress_stdout():
    from src.load_data import get_export as exp_load

# %% [markdown]
# cleanly import only the needed variables

# %%
df, df_future50 = exp_load()
dump_df(df, data_file_name='dumped_df.csv') 

# %% [markdown]
# Do your things and Enjoy!
