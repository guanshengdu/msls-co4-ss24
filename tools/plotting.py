"""
This module provides functions for displaying images using matplotlib.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

def show_image(image, title=None, ax=None, shape=None, frame=True):
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

    if ax is None:
        ax = plt.gca()

    # If the image is grayscale, use the gray colormap.
    cmap = "gray" if len(image.shape) == 2 else None

    ax.imshow(image, origin="upper", cmap=cmap)

    title = "" if title is None else title
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

    h, w = image.shape[:2]
    if frame and shape and ((h < shape[0]) or (w < shape[1])):
        rect = patches.Rectangle((0, 0), w, h, 
                                linewidth=2, 
                                edgecolor=(0.8,)*4, 
                                facecolor='none')

        # Add the rectangle patch to the plot
        ax.add_patch(rect)
        

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


def show_image_chain(*images, scale=5.0, shape=None):
    """Displays a list of images. The list of images can contain tuples of the
    form (image, title). In this case, a title is shown for the corresponding 
    image. The scale determines the figure size.

    Args:
        images: A list of images or tuples of the form (image, title).
        scale:  The scale of the figure.
        shape:  The shape of the canvas. If None, the shape is inferred 
                from the images. If "largest", the shape is set to the 
                largest image.

    Usage:
        show_image_chain(image1, image2, image3) 
        show_image_chain((image1, "title1"), image2, (image3, "title3"))
    """
    data = [(img, None) if not isinstance(img, tuple) else img for img in images]
    data = [(np.asarray(img), label) for img, label in data]
    max_shape = max(img.shape for img, _ in data)
    if shape == "largest":
        shape = max_shape
    elif isinstance(shape, int):
        shape = (shape, shape)
    fig, axes = plt.subplots(1, len(data), figsize=(scale * len(data), scale))
    for ax, (image, title) in zip(axes, data):
        show_image(image, title=title, ax=ax, shape=shape)
    plt.show()  
