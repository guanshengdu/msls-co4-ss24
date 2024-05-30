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


def show_image(image, title=None, 
               ax=None, shape=None, 
               normalize=False,
               normalize_stretch=None,
               dpi=100, 
               suppress_info=False,
               background_color=(0.93, 0.93, 0.93),
               frame=False, 
               frame_color=(0.8,)*4,
               frame_width=2,
               axes_frame=True,
               show_axes=False,
               box_aspect=None
               ):
    """Displays an image using matplotlib capabilities.

    Args:
        image: The image to display.
        title: The title of the image.
        ax:    The image axis to use. If None, a new figure is created.
        shape: The shape of the canvas. If None, the shape is inferred 
               from the image.
        normalize: If True, grayscale images are normalized so that the 
                minimal and maximal values are mapped to black and white, 
                respectively. If normalize is a 2-tuple, the provided values
                will be used for normalization (vmin, vmax = normalize). If 
                False or None, the images are displayed using the full range 
                of the current data type. If "stretch", the contrast is
                stretched using the 1% and 99% percentiles of the intensity.
        normalize_stretch: If not None, the contrast is stretched using the
                provided percentiles of the intensity. Sets normalize to True.
        frame: If True, a frame is drawn around the image (if the image
               is smaller than the canvas).
    """
    height, width = image.shape[:2]
    
    if ax is None:
        # Create a figure of the right size with 
        # one axis that takes up the full figure
        figsize = width / float(dpi), height / float(dpi)
        if figsize[0]>9 and True:
            figsize = (9, figsize[1] * 9 / figsize[0])
        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([0, 0, 1, 1])

    # If the image is grayscale, use the gray colormap.
    cmap = "gray" if len(image.shape) == 2 else None

    vmin, vmax = None, None
    if normalize_stretch is not None:
        if isinstance(normalize_stretch, (float, int)):
            normalize_stretch = (normalize_stretch, 100-normalize_stretch)
        vmin, vmax = np.percentile(image, normalize_stretch)
    elif not normalize:
        # imshow normalization is on by default!
        # If one wants to disable it, one must set vmin and vmax.
        dtype = image.dtype
        if dtype == np.uint8:
            vmin, vmax = 0, 255
        elif dtype == np.uint16:
            vmin, vmax = 0, 65535
        elif dtype in (np.float32, np.float64, float, bool):
            vmin, vmax = 0, 1.0
        else:
            assert False, "Unsupported data type: %s" % dtype
    elif isinstance(normalize, (tuple, list)) and len(normalize) == 2:
        vmin, vmax = normalize
            
    ax.imshow(image, origin="upper", cmap=cmap, vmin=vmin, vmax=vmax)

    title = "" if title is None else title
    if not suppress_info:
        title += "\n" if title else ""
        title += "(%s, %s)" % ("x".join(map(str, image.shape)), image.dtype)
    if title:
        ax.set_title(title)
    
    # Use fixed axis limits so that
    # the images are shown at scale.
    if shape is not None:
        ax.set_xlim([0, shape[1]])
        ax.set_ylim([shape[0], 0])

    # Use a background color to better see that the images are transparent.
    if background_color is None and (not show_axes):
        ax.axis("off")
    ax.set_facecolor(background_color)
    if not show_axes:
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
    ax.set_frame_on(axes_frame) 
    ax.set_anchor("N")
    if box_aspect:
        ax.set_box_aspect(box_aspect)
        # Strange hack required if box_aspect is set, but only sometimes.
        ax.update_datalim([[ax.get_xlim()[1], ax.get_ylim()[1]]])

    h, w = image.shape[:2]
    # Draw frame if:
    if frame: 
        rect = patches.Rectangle((0, 0), w, h, 
                                linewidth=frame_width, 
                                edgecolor=frame_color, 
                                facecolor='none')

        # Add the rectangle patch to the plot
        ax.add_patch(rect)  

        

def show_image_pair(image1, image2, 
                    title1=None, title2=None, 
                    normalize=True, 
                    dpi=None,
                    figsize=(6, 5),
                    shape="largest",
                    box_aspect=None,
                    frame=True,
                    **kwargs):
    """Displays a pair of images side-by-side.

    Args:
        image1: The first image.
        image2: The second image.
        title1: The title of the first image.
        title2: The title of the second image.
        frame:  If True, a frame is drawn around the images 
                (if the images are smaller than the canvas).
                Set "forced" to force a frame.
    """
    # This converts PIL images to numpy arrays.
    image1 = np.asarray(image1)
    image2 = np.asarray(image2)

    max_shape = (max(image1.shape[0], image2.shape[0]),
                 max(image1.shape[1], image2.shape[1]))
    
    if dpi is not None:
        # Overrides figsize
        figsize = (max_shape[0]/dpi, max_shape[1]/dpi)

    if shape=="largest":
        shape = max_shape

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    draw_frame1 = ((frame=="forced") or 
                   (frame and shape is not None and shape!=image1.shape[:2]))
    draw_frame2 = ((frame=="forced") or 
                   (frame and shape is not None and shape!=image2.shape[:2]))
    
    show_image(image1, title1, ax1, 
               normalize=normalize, 
               shape=shape, 
               box_aspect=box_aspect,
               frame=draw_frame1,
               **kwargs)
    show_image(image2, title2, ax2, 
               normalize=normalize, 
               shape=shape, 
               box_aspect=box_aspect,
               frame=draw_frame2,
               **kwargs) 
    fig.tight_layout()


def show_image_chain(images, **kwargs):
    """Displays a list of images. Equivalent to show_image_grid(..., ncols=-1).
    """
    kwargs.setdefault("ncols", -1)
    return show_image_grid(images, **kwargs) 


def show_image_grid(images, titles=None, 
                    ncols=3, 
                    scale=4.0, 
                    figsize=None, 
                    shape="largest",
                    dpi=100,
                    suppress_info=False,
                    normalize=True,
                    box_aspect=None,
                    frame=True,
                    **kwargs):
    """Displays a grid of images. The width of the grid is determined by ncols.

    Args:
        images: A list of images, a generator of images, or a dictionary of
                titles and images.
        titles: A list of titles for the images (optional). If images are 
                provided as a dictionary, the titles are inferred from the
                dictionary keys.
        ncols:  The number of columns in the grid. If ncols=-1, the number of 
                columns is set to the number of images.
        scale:  The scale of the figure.
        figsize: The size of the figure. (Overrides scale.)
        shape:  The shape of the image canvas. Default: "largest". If 
                "largest", the shape is set to the largest image, and all 
                images are shown at the same scale. If None, the shape is 
                inferred from the images. 
        dpi:    The DPI of the figure. Default: 100. Only relevant if
                figsize is not set. The real DPI will not be exactly 
                the same as the requested DPI.
        suppress_info: If True, the image shape and data type are not shown
                in the title.
        normalize: If True, grayscale images are normalized so that the 
                minimal and maximal values are mapped to black and white, 
                respectively. If normalize is a 2-tuple, the provided values
                will be used for normalization (vmin, vmax = normalize). If 
                False or None, the images are displayed using the full range 
                of the current data type. 
        box_aspect: If not None, the aspect ratio of the image is fixed.
                Useful for images with different aspect ratios.
        frame:  If True, a frame is drawn around the images (if the images
                are smaller than the canvas). Set "forced" to force a frame.
        kwargs:  Additional keyword arguments passed to show_image().
        
    Usage:
        show_image_grid([image1, image2, image3]) 
        show_image_grid({title1: image1, title2: image2, title3: image3})
    """
    if not images:
        return
    
    # Manage input types
    import types
    if isinstance(images, types.GeneratorType):
        images = list(images)
    elif isinstance(images, dict):
        titles = list(images.keys())
        images = list(images.values())
    if isinstance(titles, types.GeneratorType):
        titles = list(titles)
    elif titles is None:
        titles = [None] * len(images)
    
    images = [None if img is None else np.asarray(img) for img in images]
    assert titles is None or (len(images) == len(titles))
    has_titles = any(titles)

    # Number of rows and columns
    if ncols == -1:
        ncols = len(images)
        nrows = 1
    else:
        ncols = min(len(images), ncols)
        nrows = int(np.ceil(len(images) / ncols))

    # Manage shape
    h_max, w_max = np.vstack([ img.shape[:2] for img in images if img is not None ]).max(axis=0)
    
    # Height of title in inches
    h_title = (has_titles*1 + (not suppress_info)*0.5)*scale
    h_fig = (h_max / dpi * scale + h_title)*nrows
    w_fig = (w_max / dpi * scale)*ncols

    if shape == "largest":
        shape = (h_max, w_max)

    # Figure size
    if figsize is None:
        figsize = (w_fig, h_fig)
    # Limit the figure size to 9 inches in width.
    # this is a good size for printing
    if figsize[0]>9:
        figsize = (9, figsize[1] * 9 / figsize[0])

    # Create the figure
    fig, axes = plt.subplots(nrows, ncols, 
                             figsize=figsize,
                             squeeze=False)
    
    for ax, image, title in zip(axes.flat, images, titles):    
        if image is None:
            ax.axis("off")
            continue        
        draw_frame = ((frame=="forced") or 
                      (frame and shape is not None and shape!=image.shape[:2]))
        show_image(image, title=title, ax=ax, 
                   suppress_info=suppress_info, 
                   normalize=normalize,
                   box_aspect=box_aspect,
                   shape=shape,
                   frame=draw_frame,
                   **kwargs)
        
    # Disable grid axes that are not used
    for i in range(len(images), len(axes.flat)):
        axes.flat[i].axis("off")
    fig.tight_layout()
    return fig


def save_figure(fig=None, path="figure.pdf", **kwargs):
    if fig is None:
        fig = plt.gcf()
    kwargs.setdefault("transparent", True)
    kwargs.setdefault("bbox_inches", "tight")
    kwargs.setdefault("dpi", 300)
    path = Path(path)
    ensure_dir(path.parent)
    plt.savefig(path, **kwargs)
