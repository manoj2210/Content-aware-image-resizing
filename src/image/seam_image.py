import numpy as np
from src.energy_filter import energy_function

__all__ = ['Image']


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
    def energy_map(img, fn):
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

    def remove_seam(self, seam):
        """
        Function to remove the seam
        Args:
            seam: 1-D numpy.array seam to remove. Output of seam function

        Returns:
            3-D numpy array of the image that is 1 pixel shorter in width than the input img
        """
        height, width = self.energy_image.shape[:2]
        return np.array([np.delete(self.energy_image[row], seam[row], axis=0) for row in range(height)])

    def find_energy_of_image(self):
        self.energy_image = self.energy_map(self.cropped_image, energy_function)

    def cumulative_energy(self):
        """
        Returns:
            tuple of 2 2-D numpy.array(int64) with shape (height, width).

            paths has the x-offset of the previous seam element for each pixel.

            path_energies has the cumulative energy at each pixel.
        """
        height, width = self.energy_image.shape
        paths = np.zeros((height, width), dtype=np.int64)
        path_energies = np.zeros((height, width), dtype=np.int64)
        path_energies[0] = self.energy_image[0]
        paths[0] = np.arange(width) * np.nan

        for i in range(1, height):
            for j in range(width):
                prev_energies = path_energies[i - 1, max(j - 1, 0):j + 2]
                least_energy = prev_energies.min()
                path_energies[i][j] = self.energy_image[i][j] + least_energy
                paths[i][j] = np.where(prev_energies == least_energy)[0][0] - (1 * (j != 0))

        return paths, path_energies
