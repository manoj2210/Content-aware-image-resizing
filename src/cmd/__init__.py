import argparse

__all__ = ['arguments']
parser = argparse.ArgumentParser(description="Resize Image with content Awareness")
parser.add_argument('input_file')
parser.add_argument('-a', '--axis', required=True,
                    help="What axis to shrink the image on.", choices=['x', 'y'])
parser.add_argument('-p', '--pixels', type=int, required=True,
                    help="How many pixels to shrink the image by.")
parser.add_argument('-o', '--output',
                    help="What to name the new cropped image.")
parser.add_argument('-i', '--interval', type=int,
                    help="Save every i intermediate images.")
parser.add_argument('-s', '--show_seam', type=bool,
                    help="Whether to highlight the removed seam on the intermediate images.")

arguments = vars(parser.parse_args())
