from src.cmd import arguments
from src.image import seam_image
from src.helpers.utils import get_img_arr, display_image

image = seam_image.Image(get_img_arr('images/'+arguments['input_file']))
display_image(image.resize_image(2,arguments['file_type']))
print(arguments)
