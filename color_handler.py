from PIL import Image
import numpy as np
from colormap import rgb2hex


class PaletteGenerator:
    def __init__(self, imagefile):
        self.image_file = imagefile
        self.my_img = Image.open(self.image_file)
        self.my_img_array = np.array(self.my_img)
        self.top_colors = []
        print(f"shape of the image: {self.my_img_array.shape}")

    def get_pixels(self):
        copy_img = self.my_img.resize(size=(100, 100), resample=Image.NEAREST)
        width, height = copy_img.size
        color_dict = {}
        for x in range(1, width):
            for y in range(1, height):
                rgb = copy_img.getpixel((x, y))
                try:
                    color_dict[rgb] += 1
                except KeyError:
                    color_dict[rgb] = 1

        top_numbers = [x for x in color_dict.values()]
        top_numbers.sort(reverse=True)
        top_ten = top_numbers[:144:12]
        top_rgbs = []
        for color in top_ten:
            x = [k for k, v in color_dict.items() if v == color][0]
            top_rgbs.append(x)
            color_dict.pop(x)
        for c in top_rgbs:
            hex = rgb2hex(c[0], c[1], c[2])
            self.top_colors.append(hex)
        print(f"length: {len(self.top_colors)}\nhex: {self.top_colors}")
