# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 22:26:20 2020

@author: basheer669
"""


pixel_energies=[
    [9, 9, 0, 9, 9],
    [9, 1, 9, 8, 9],
    [9, 9, 9, 9, 0],
    [9, 9, 9, 0, 9],]



class SeamEnergyWithBackPointer():
    def __init__(self, energy, x_coordinate_in_previous_row=None):
        self.energy = energy
        self.x_coordinate_in_previous_row = x_coordinate_in_previous_row

seam_energies = []
# Initialize the top row of seam energies by copying over the top
# row of the pixel energies. There are no back pointers in the
# top row.
seam_energies.append([
    SeamEnergyWithBackPointer(pixel_energy)
    for pixel_energy in pixel_energies[0]])


# Skip the first row in the following loop.
for y in range(1, len(pixel_energies)):
    pixel_energies_row = pixel_energies[y]
    seam_energies_row = []
    for x, pixel_energy in enumerate(pixel_energies_row):
        # Determine the range of x values to iterate over in the
        # previous row. The range depends on if the current pixel
        # is in the middle of the image, or on one of the edges.
        x_left = max(x - 1, 0)
        x_right = min(x + 1, len(pixel_energies_row) - 1)
        x_range = range(x_left, x_right + 1)
        min_parent_x = min(
            x_range,
            key=lambda x_i: seam_energies[y - 1][x_i].energy
        )
        min_seam_energy = SeamEnergyWithBackPointer(
            pixel_energy + seam_energies[y - 1][min_parent_x].energy,
            min_parent_x
        )
        seam_energies_row.append(min_seam_energy)
    seam_energies.append(seam_energies_row)
# Find the x coordinate with minimal seam energy in the bottom row.
min_seam_end_x = min(
    range(len(seam_energies[-1])),
    key=lambda x: seam_energies[-1][x].energy
)

# Follow the back pointers to form a list of coordinates that
# form the lowest-energy seam.
seam = []
seam_point_x = min_seam_end_x
for y in range(len(seam_energies) - 1, -1, -1):
    seam.append((seam_point_x, y))
    seam_point_x = \
        seam_energies[y][seam_point_x].x_coordinate_in_previous_row
seam.reverse()
#print(pixel_energies)
print(seam)