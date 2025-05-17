import numpy as np
import imageio.v3 as iio

def load_image(image_path):
    image = iio.imread(image_path).astype(np.uint16)
    return image

def differential_encoding(image):
    diff_image = np.zeros_like(image, dtype=np.int16)
    # First column as reference
    diff_image[:, 0] = image[:, 0]
    # Iterate over columns
    for i in range(1, image.shape[1]):
        diff_image[:, i] = image[:, i] - image[:, i - 1]
    return diff_image

def differential_decoding(diff_image):
    decoded_image = np.zeros_like(diff_image, dtype=np.int16)
    # First column as reference
    decoded_image[:, 0] = diff_image[:, 0]
    # Iterate over columns
    for i in range(1, diff_image.shape[1]):
        decoded_image[:, i] = decoded_image[:, i - 1] + diff_image[:, i]
    return decoded_image

