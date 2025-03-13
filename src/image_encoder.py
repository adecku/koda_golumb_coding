import numpy as np
import bitarray
import bitarray.util
from data_operations import load_image, differential_encoding, differential_decoding
from exp_golomb_coder import ExpGolombCoder
from golomb_coder import GolombCoder


def encode_image(image_path, output_path, method, param):

    image = load_image(image_path)

    diff_image = differential_encoding(image)
    # Inicjalizacja strumienia bitowego do przechowywania zakodowanych danych

    bitstream = bitarray.bitarray()

    if method == 'golomb':
        coder = GolombCoder(param)
    elif method == 'exp-golomb':
        coder = ExpGolombCoder(param)
    else:
        raise ValueError("Nieprawidlowa nazwa metody")

    # kodowanie pikseli obrazu
    for row in diff_image:
        for pixel in row:
            encoded_pixel = coder.encode(pixel)
            # Konwersja zakodowanego ciągu znakowego na bitarray i dodanie go do strumienia bitowego

            bitstream.extend(bitarray.bitarray(encoded_pixel))
    # Zapis do pliku jako ciąg znaków
    with open(output_path, "w") as f:
        f.write(bitstream.to01())


encode_image(
    "../data/obrazy_testowe/mandril.pgm",
    "../data/obrazy_testowe/mandril_bit.txt",
    "golomb",
    4
)
