from contextlib import contextmanager
import sys, os

@contextmanager
def suppress_stdout():
    """Suppress any output

    with suppress_stdout():
        import module_that_print_things
    """
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


# Equivalent for Notebooks:
# from IPython.utils import io
# with io.capture_output() as captured:
#     %run 1.load_data.ipynb
#     # print captured.stdout # prints stdout from your script