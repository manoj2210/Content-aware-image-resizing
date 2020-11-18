# from src.cmd import arguments
#
# print(arguments)

from src.image import seam_image
from src.helpers.utils import get_img_arr,display_image

image = seam_image.Image(get_img_arr('images/sample.png'))
display_image(image.raw_image)
image.find_energy_of_image(image.raw_image)
display_image(image.energy_image)
