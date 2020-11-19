# from src.cmd import arguments
#
# print(arguments)

from src.image import seam_image
from src.helpers.utils import get_img_arr, display_image

image = seam_image.Image(get_img_arr('images/sample.jpeg'))
display_image(image.resize_image(100))
