import numpy as np
from src.energy_filter import energy_function
# import numba

__all__ = ['Image']

from src.helpers.utils import save_image_with_options, highlight_seam, display_image
from src.least_energy import min_energy_seam


class Image:
    def __init__(self, image: np.ndarray):
        self.raw_image = image
        self.energy_image = image
        self.cropped_image = image

    @staticmethod
    def get_neighbors(img: np.ndarray, row: int, col: int):
        """
        Function to get the adjacent neighbours
        Args:
            img: 3-D numpy.array the image
            row: int
            col: int

        Returns:
            tuple of 3 1-D numpy arrays [r,g,b]
               y0
            x0 -- x1
               y1
        """
        height, width = img.shape[:2]

        if row == 0:
            y0 = img[height - 1][col]
            y1 = img[row + 1][col]
        elif row == height - 1:
            y0 = img[row - 1][col]
            y1 = img[0][col]
        else:
            y0 = img[row - 1][col]
            y1 = img[row + 1][col]

        if col == 0:
            x0 = img[row][width - 1]
            x1 = img[row][col + 1]
        elif col == width - 1:
            x0 = img[row][col - 1]
            x1 = img[row][0]
        else:
            x0 = img[row][col - 1]
            x1 = img[row][col + 1]

        return x0, x1, y0, y1

    @staticmethod
    def energy_map(img: np.ndarray, fn) -> np.ndarray:
        """

        Args:
            img: numpy.array with shape (height, width, 3)
            fn: The energy function to use. Should take in 4 pixels and return a float.

        Returns:
            The energy function to use. Should take in 4 pixels and return a float.

        """
        x0 = np.roll(img, -1, axis=1).T
        x1 = np.roll(img, 1, axis=1).T
        y0 = np.roll(img, -1, axis=0).T
        y1 = np.roll(img, 1, axis=0).T

        # we do a lot of transposing before and after here because sums in the
        # energy function happen along the first dimension by default when we
        # want them to be happening along the last (summing the colors)
        return fn(x0, x1, y0, y1).T

    @staticmethod
    def remove_seam(img: np.ndarray, seam: list) -> np.ndarray:
        """
        Function to remove the seam
        Args:
            img: Raw image
            seam: 1-D numpy.array seam to remove. Output of seam function

        Returns:
            3-D numpy array of the image that is 1 pixel shorter in width than the input img
        """
        height, width = img.shape[:2]
        return np.array([np.delete(img[row], [x for x in seam if x[1] == row][0][0]-1, axis=0) for row in range(height)])

    def find_energy_of_image(self, img: np.ndarray) -> np.ndarray:
        return self.energy_map(img, energy_function)

    @staticmethod
    def cumulative_energy(img):
        """
        Returns:
            tuple of 2 2-D numpy.array(int64) with shape (height, width).

            paths has the x-offset of the previous seam element for each pixel.

            path_energies has the cumulative energy at each pixel.
        """
        height, width = img.shape
        paths = np.zeros((height, width), dtype=np.int64)
        path_energies = np.zeros((height, width), dtype=np.int64)
        path_energies[0] = img[0]
        paths[0] = np.arange(width) * np.nan

        for i in range(1, height):
            for j in range(width):
                prev_energies = path_energies[i - 1, max(j - 1, 0):j + 2]
                least_energy = prev_energies.min()
                path_energies[i][j] = img[i][j] + least_energy
                paths[i][j] = np.where(prev_energies == least_energy)[0][0] - (1 * (j != 0))

        return paths, path_energies

    # @staticmethod
    # def seam_end(energy_totals: np.ndarray):
    #     """
    #     Args:
    #         energy_totals:  2-D numpy.array(int64)
    #         Cumulative energy of each pixel in the image
    #
    #     Returns:
    #         numpy.int64
    #         the x-coordinate of the bottom of the seam for the image with these
    #         cumulative energies
    #
    #     """
    #     return list(energy_totals[-1]).index(min(energy_totals[-1]))
    #
    # @staticmethod
    # def find_seam(paths: np.ndarray, end_x: list[int]):
    #     """
    #
    #     Args:
    #         paths: 2-D numpy.array(int64)
    #             Output of cumulative_energy_map. Each element of the matrix is the offset of the index to
    #             the previous pixel in the seam
    #         end_x: int
    #             The x-coordinate of the end of the seam
    #
    #     Returns:
    #         1-D numpy.array(int64) with length == height of the image
    #         Each element is the x-coordinate of the pixel to be removed at that y-coordinate. e.g.
    #         [4,4,3,2] means "remove pixels (0,4), (1,4), (2,3), and (3,2)"
    #     """
    #     height, width = paths.shape[:2]
    #     seam = [end_x]
    #     for i in range(height - 1, 0, -1):
    #         cur_x = seam[-1]
    #         offset_of_prev_x = paths[i][cur_x]
    #         seam.append(cur_x + offset_of_prev_x)
    #     seam.reverse()
    #     return seam

    # @numba.jit()
    def resize_image(self, cropped_pixels):
        """
        Resizes the image
        Args:
            cropped_pixels: int
                Number of pixels you want to shave off the width. Aka how many vertical seams to remove.

        Returns:
             3-D numpy array of your now cropped_pixels-slimmer image.
        """
        img = self.raw_image.copy()
        for i in range(cropped_pixels):
            energy_image = self.find_energy_of_image(img)
            seam1 = min_energy_seam(energy_image)
            img = self.remove_seam(img, seam1)
            save_image_with_options(img, 1, seam1, 0, str(i) + 'th.jpeg')
        return img
