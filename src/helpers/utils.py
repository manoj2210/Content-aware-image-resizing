import numpy as np
from PIL import Image
from typing import List


def get_img_arr(filename: str) -> np.ndarray:
    """
    Function to get the image array

    Args:
        filename (str): File path (png or jpg)

    Returns:
        np.array: Numpy array of pixels of the image
    """
    return np.array(Image.open(filename))


def display_image(img: np.ndarray):
    """
    Function to display the image
    Args:
        img (np.array): Image array

    Returns:
        Nothing
    """
    Image.fromarray(img).show()


def display_energy_map(img: np.ndarray):
    """
    Function to display the energy map

    Args:
        img (np.array): Image array

    Returns:
        Nothing
    """
    scaled = img * 255 / img.max()
    energy = Image.fromarray(scaled).show()


def highlight_seam(img: np.ndarray, seam: np.ndarray) -> np.array:
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


def save_image_with_options(img: np.ndarray, highlight: bool, seam: np.ndarray, rotated: bool,
                            save_name: str, point: np.ndarray, save_points: List[np.ndarray]):
    """
    Function to the save the image
    Args:
        img: Image array
        highlight:  Whether to draw the seam to be removed on the image
        seam: Set of points with low energy
        rotated: Whether the image is rotated or not
        save_name: Name of the file to be saved
        point: one of the point in the seam
        save_points: list of points to be carved

    Returns:
        void
    """
    if highlight:
        img = highlight_seam(img, seam)
    if rotated:
        img = Image.fromarray(np.transpose(img, axes=(1, 0, 2)))
    else:
        img = Image.fromarray(img)
    base, ext = save_name.split('.')
    img.save(base + '/' + base.split('/')[-1] + '_' + str(point).zfill(len(str(save_points[-1]))) + '.' + ext)
