# Modular Jupyter Notebooks Starter

A simple starter showing how to modularize Jupyter notebooks, import external py modules and use you code editor to refactor anything.


## Install Conda

As first step let's install [Anaconda](https://www.anaconda.com/) for our platform.

Conda will modify your `.bash_profile` or similar bash startup file, by adding something similar to this block:

```bash
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
CONDA_ROOT=/usr/local/anaconda3
__conda_setup="$('$CONDA_ROOT/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "$CONDA_ROOT/etc/profile.d/conda.sh" ]; then
        . "$CONDA_ROOT/etc/profile.d/conda.sh"
    else
        export PATH="$CONDA_ROOT/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
```

By default conda will always activate its `base` virtualenv anytime you lauch a shell.  
If you don't want that just add this line to your `.bash_profile` before the block added by conda:

```bash
export CONDA_AUTO_ACTIVATE_BASE=false
```

## Create a virtualenv

It's not wise to install all your packages into the `base` environment. Also, as a general rule, any new project should have its own virtualenv or at least, reuse one for general purpose.
So let's create a new one by cloning from the base env (usually the best solution):

```bash
# conda create --clone ENV_FROM --name NEW_ENV
conda create --clone base --name my_new_env
```

To activate/deactivate a virtual env:

```bash
conda activate my_new_env
conda deactivate
```

To list all your envs:

```bash
conda env list
```

## Launch the Jupyter Server

```bash
cd notebooks
conda activate my_new_env
# launch the server
jupyter notebook
```


## Jupytext
I've always worked with standard python, so I was a bit confused by the development environment inside the browser. Jupyter Notebooks offer cool visualization and interactinve features but they don't offer the best DX.
The feature I miss most is refactoring tool (like renaming a variable) or the highlighting of all the occurrences of a certain variable.  
But after some exploration [jupytext](https://github.com/mwouts/jupytext) came to the rescue.

Jupytext is a plugin for Jupyter that can save Jupyter notebooks as plain python script and vice-versa. That means that you can create and work on your notebook normally from the browser and if you want to refactor something you can open the generated script, modify this one on your code editor and when saved it generates an updated version of your original notebook. More info on the [project documentation](https://jupytext.readthedocs.io/en/latest/paired-notebooks.html).

After activating your env, install jupytext with:

```bash
conda install jupytext -c conda-forge
```

By default you should create your notebooks in the `notebooks` dir and the scripts will be generated in the `src` dir.

You can modify where the notebooks and script are located by modifying the [`jupytex.toml`](https://jupytext.readthedocs.io/en/latest/config.html) file.


## Modularization
Given that now you could execute both the notebooks and the scripts independently I wanted to modularize my code and put all the reusable modules somewhere in a __common__ location that would be accessible from both the notebooks and the scripts.

Unfortunately, there is no easy way to modularize your notebooks as you would in plain ol' python.
So, here's my tricky (but working) solution: in the notebooks directory there are two python modules that are symlinked from the `src` directory: `loader` and `reloader`. These are symlinked because I need them to be inside both the `src` and the `notebooks` dirs and I don't want to maintain two copies of them.

### loader
As you would expect, the `loader` module lets you load external python modules (living outside the `notebooks` dir but inside your project root dir). This work by modifying your `syspath` to include the top level directory of the project.
The only thing to **remember is to import this module into any notebooks that need to access external modules**.

### reloader
This optional modules is quite useful anytime you modify any imported external module. Normally to make this work you would need to restart your jupyter server, but with this simple trick you don't need to:

1. Into your notebook import the reloader `import reloader`
2. Modify your external module, example `lib/figure.py`
3. From your notebook execute a cell containing `reloader.clear()`
4. Keep on working on you notebook

## Configuration
I've made some assumption on where the dataset and generated code should live, but this is entirely configurable. All the options can be changed by editing the `config.toml` file.

## Common functions (lib)
Inside the `lib` directory there are some reusable common functions that I need to reuse from project to project. This modules are a WIP and they will probably expand over time. This is just my personal configuration, fell free to ignore this directory if you don't need it.
The modules inside `lib` are scoped my pseudonime of the python lib the functions refer to, for for example the reusable `pandas` function are into `lib/pd` or the matplotlib functions are into `lib/plt`.

## Import generated scrips into your notebooks
Another cool feature of Jupytex is that once it generates a script from a notebook, you can then import that script into another notebook 🤯

And thanks to the `loader` introduced above you just need to do this:

```python
import loader
from src import load_data
```

### Suppress output when importing scripts

If your notebook generates output then that output will be visible when you import the corresponding generated script. Most of the times you don't need this, so here's a couple of strategy about that.

`suppress_stdout` is a helper context manager I've defined, it suppress the output from `print` and pandas output

```python
with suppress_stdout():
    from src.load_data import get_export as exp_load
```

Unfortunately it seems ineffective for generated matplotlib pictures.
So when `suppress_stdout` won't work you can use this instead:

```python
with io.capture_output() as captured:
    # Script that generated pyplot figures
    from src.correlation import get_export as exp_corr
```

TODO: a better strategy to suppress anything!

### Don't commit the notebooks to your repo
A side effect of Jupytext generated scripts is that now you could simply commit these instead of the notebooks.
They still preserve any output and once you launch your jupyter server it will re-create your notebooks. Read more on [how and why to use Jupytext](https://jupytext.readthedocs.io/en/latest/examples.html).

For this git repo the notebooks are tracked by git in order to show you usage example but just uncomment `# notebooks/**.ipynb` from `.gitignore` to never track notebooks and track the `src/` scripts instead.

## Example Dataset
Dataset obtained from https://www.kaggle.com/michau96/restaurant-business-rankings-2020 under CC0: Public Domain license.


## Alternative
Another way you to import common functions into both your notebooks and scripts is by pip-installing a local directory as a development package.

- Put all your common functions in a dir, for example `lib`
- create a [setup script](https://docs.python.org/3/distutils/setupscript.html)
- install it with pip in dev mode

```bash
conda activate my_env
cd lib
pip install -e
```

The limitation with this is that you can't freely import your generated script that aren't located in the same directory of the notebooks.
If you like your notebooks and generated script in two different dirs (as I would for clean separation) then you can use my system defined above.


## Explore the Notebooks
Take a look at the notebooks in `notebooks` and see by yourself what they can do.


## About

Use this responsibly.
Comments and PRs are welcome!

Enjoy
