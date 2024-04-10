__version__ = "0.1"
__author__ = "Norman Juchler"

from .plotting import (display_image,
                       draw_image, # Obsolete, use show_image 
                       show_image,
                       show_image_pair, 
                       show_image_chain, 
                       show_image_grid,
                       save_figure)
from .colors import color_palette, colors2plotly
from .fileio import load_audio, ensure_dir

PALETTE = color_palette("default", alpha=[1.00, 0.45, 0.15])
PALETTE_RGB = [PALETTE[1], PALETTE[2], PALETTE[0]]
PALETTE_PLOTLY = colors2plotly(PALETTE)

# Set default color palette
import matplotlib.pyplot as plt
plt.rcParams["axes.prop_cycle"] = plt.cycler(color=PALETTE)
#plt.rcParams["figure.figsize"] = (5, 3)
#plt.rcParams["figure.dpi"] = 300
