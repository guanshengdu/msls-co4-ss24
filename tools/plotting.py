"""
This module provides functions for displaying images using matplotlib.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from .fileio import ensure_dir
from pathlib import Path


def display_image(image=None, scale=None):
    """Displays an image using IPython capabilities."""
    from IPython.display import display
    import PIL.Image
    if isinstance(image, (str, Path)):
        image = PIL.Image.open(image)
    if not isinstance(image, PIL.Image.Image):
        image = PIL.Image.fromarray(image)
    if scale is not None:
        image = image.resize((int(image.width * scale), 
                              int(image.height * scale)))
    display(image)

    

def draw_image(image, **kwargs):
    """Alias for show_image()"""
    return show_image(image, **kwargs)


def show_image(image, title=None, ax=None, shape=None, 
               frame=True, dpi=100, suppres_info=False):
    """Displays an image using matplotlib capabilities.

    Args:
        image: The image to display.
        title: The title of the image.
        ax:    The image axis to use. If None, a new figure is created.
        shape: The shape of the canvas. If None, the shape is inferred 
               from the image.
        frame: If True, a frame is drawn around the image (if the image
               is smaller than the canvas).
    """
    #background_color = "lightgray"
    background_color = (0.93, 0.93, 0.93)

    height, width = image.shape[:2]
    
    if ax is None:
        # Create a figure of the right size with 
        # one axis that takes up the full figure
        figsize = width / float(dpi), height / float(dpi)
        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([0, 0, 1, 1], frame_on=False)

        #_, ax = plt.subplots()

    # If the image is grayscale, use the gray colormap.
    cmap = "gray" if len(image.shape) == 2 else None

    ax.imshow(image, origin="upper", cmap=cmap)

    title = "" if title is None else title
    if not suppres_info:
        title += "\n(%s, %s)" % ("x".join(map(str, image.shape)), image.dtype)
    if title:
        ax.set_title(title)
    
    # Use fixed axis limits so that
    # the images are shown at scale.
    if shape is not None:
        ax.set_xlim([0, shape[0]])
        ax.set_ylim([shape[1], 0])

    # Use a background color to better see that the images are transparent.
    ax.set_facecolor(background_color)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.axis("off")

    h, w = image.shape[:2]
    if frame and shape and ((h < shape[0]) or (w < shape[1])):
        rect = patches.Rectangle((0, 0), w, h, 
                                linewidth=2, 
                                edgecolor=(0.8,)*4, 
                                facecolor='none')

        # Add the rectangle patch to the plot
        ax.add_patch(rect)

    fig = ax.get_figure()
    fig.tight_layout()
        

def show_image_pair(image1, image2, title1=None, title2=None, shape="largest"):
    """Displays a pair of images side-by-side.

    Args:
        image1: The first image.
        image2: The second image.
        title1: The title of the first image.
        title2: The title of the second image.
        shape:  The shape of the canvas. If None, the shape is inferred 
                from the images. If "largest", the shape is set to the 
                largest image.
    """
    # This converts PIL images to numpy arrays.
    image1 = np.asarray(image1)
    image2 = np.asarray(image2)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    if shape=="largest":
        shape = max(image1.shape, image2.shape)
    elif isinstance(shape, int):
        shape = (shape, shape)
    show_image(image1, title1, ax1, shape=shape)
    show_image(image2, title2, ax2, shape=shape)
    plt.show()


def show_image_chain(images, titles=None, scale=5.0, figsize=None, shape=None):
    """Displays a list of images. The list of images can contain tuples of the
    form (image, title). In this case, a title is shown for the corresponding 
    image. The scale determines the figure size.

    Args:
        images: A list of images or tuples of the form (image, title).
        titles: A list of titles for the images (optional).
        scale:  The scale of the figure.
        figsize: The size of the figure. (Overrides scale.)
        shape:  The shape of the canvas. If None, the shape is inferred 
                from the images. If "largest", the shape is set to the 
                largest image.

    Usage:
        show_image_chain(image1, image2, image3) 
        show_image_chain((image1, "title1"), image2, (image3, "title3"))
    """
    show_image_grid(images, titles=titles, ncols=-1, scale=scale, figsize=figsize, shape=shape) 


def show_image_grid(images, titles=None, ncols=3, scale=4.0, 
                    figsize=None, shape=None, suppress_info=False):
    """Displays a grid of images. The list of images can contain tuples of the
    form (image, title). In this case, a title is shown for the corresponding 
    image. The scale determines the figure size.

    Args:
        images: A list of images or tuples of the form (image, title).
        titles: A list of titles for the images (optional).
        ncols:  The number of columns in the grid (if -1: ncols = len(images)).
        scale:  The scale of the figure.
        figsize: The size of the figure. (Overrides scale.)
        shape:  The shape of the canvas. If None, the shape is inferred 
                from the images. If "largest", the shape is set to the 
                largest image.

    Usage:
        show_image_grid(image1, image2, image3) 
        show_image_grid((image1, "title1"), image2, (image3, "title3"))
    """
    if titles is not None:
        assert len(images) == len(titles)
        images = list(zip(images, titles))
    data = [(img, None) if not isinstance(img, tuple) else img for img in images]
    data = [(np.asarray(img), label) for img, label in data]
    max_shape = max(img.shape for img, _ in data)
    if shape == "largest":
        shape = max_shape
    elif isinstance(shape, int):
        shape = (shape, shape)
    if ncols == -1:
        ncols = len(data)
        nrows = 1
    else:
        ncols = min(len(data), ncols)
        nrows = int(np.ceil(len(data) / ncols))
    if figsize is None:
        figsize = (scale * ncols, scale * nrows)
    # Limit the figure size to 9 inches in width.
    # this is a good size for printing.
    if figsize[0]>9:
        figsize = (9, figsize[1] * 9 / figsize[0])
    fig, axes = plt.subplots(nrows, ncols, 
                             figsize=figsize,
                             )
    for ax, (image, title) in zip(axes.flat, data):
        show_image(image, title=title, ax=ax, shape=shape, 
                   suppres_info=suppress_info)
    for i in range(len(data), len(axes.flat)):
        axes.flat[i].axis("off")
    plt.show()


def save_figure(fig=None, path="figure.pdf", **kwargs):
    if fig is None:
        fig = plt.gcf()
    kwargs.setdefault("transparent", True)
    kwargs.setdefault("bbox_inches", "tight")
    kwargs.setdefault("dpi", 300)
    path = Path(path)
    ensure_dir(path.parent)
    plt.savefig(path, **kwargs)
