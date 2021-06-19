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

# %%
from pathlib import Path
from sys import path as syspath

CWD = Path().resolve()
PROJECT_ROOT = CWD.parents[0]

proj_root = str(PROJECT_ROOT)
if not proj_root in syspath:
    syspath.append(proj_root)



# %%
def show_importables(search_path=['.']):
    """Get a list of all importable modules from a given path

    https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html

    Args:
        search_path (list, optional): set to None to see all modules importable from sys.path. Defaults to ['.'].
    """
    import pkgutil
    all_modules = [x[1] for x in pkgutil.iter_modules(path=search_path)]
    print(all_modules)
