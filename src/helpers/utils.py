import numpy as np
from PIL import Image


def get_img_arr(filename: str) -> np.array:
    """
    Function to get the image array

    Args:
        filename (str): File path (png or jpg)

    Returns:
        np.array: Numpy array of pixels of the image
    """
    return np.array(Image.open(filename))


def display_image(img: np.array):
    """
    Function to display the image
    Args:
        img (np.array): Image array

    Returns:
        Nothing
    """
    Image.fromarray(img).show()


def display_energy_map(img: np.array):
    """
    Function to display the energy map

    Args:
        img (np.array): Image array

    Returns:
        Nothing
    """
    scaled = img * 255 / img.max()
    energy = Image.fromarray(scaled).show()


def highlight_seam(img: np.array, seam: np.array) -> np.array:
    """
        Function to highlight the seam

    Args:
        img (np.array): Image array
        seam (np.array): Seam array with length equals height of the image array
        The x-coordinates of the pixel to remove from each row

    Returns:
        Image array with seam highlighted
    """
    if len(seam) != img.shape[0]:
        err_msg = "Seam height {0} does not match image height {1}"
        raise ValueError(err_msg.format(img.shape[0], len(seam)))
    highlight = img.copy()
    height, width = img.shape[:2]
    for i in range(height):
        j = seam[i]
        highlight[i][j] = np.array([255, 0, 0])
    return highlight
