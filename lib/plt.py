from lib.constants import IMAGE_DIR_PATH
from pathlib import Path

import matplotlib.pyplot as plt

# Figures
def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300, **kwargs):
    img_path = Path(IMAGE_DIR_PATH, fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(img_path, format=fig_extension, dpi=resolution, **kwargs)
