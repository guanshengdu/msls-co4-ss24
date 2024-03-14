__version__ = "0.1"
__author__ = "Norman Juchler"

from .plotting import (show_image, show_image_pair, show_image_chain)
from .colors import color_palette
from .fileio import ensure_dir
from .system_info import print_system_info

DEFAULT_PALETTE = color_palette("default", alpha=[1.00, 0.45, 0.15])

# Set default color palette
import matplotlib.pyplot as plt
plt.rcParams["axes.prop_cycle"] = plt.cycler(color=DEFAULT_PALETTE)
#plt.rcParams["figure.figsize"] = (5, 3)
plt.rcParams["figure.dpi"] = 300
