import numpy as np

from golomb_coder import GolombCoder
from exp_golomb_coder import ExpGolombCoder
from data_operations import *

if __name__ == '__main__':
    print("GOLOMB")
    coder = GolombCoder(7)
    encoded = coder.encode(17)
    print(encoded)
    decoded = coder.decode(encoded)
    print(decoded)

    # ---------------------------------------------
    print("EXP GOLOMB")
    exp_coder = ExpGolombCoder(0)
    encoded = exp_coder.encode(10)
    print(encoded)
    decoded = exp_coder.decode(encoded)
    print(decoded)

    # ---------------------------------------------
    image = load_image("../data/obrazy_testowe/mandril.pgm")
    print(image)
    diff_image = differential_encoding(image)
    print(diff_image)
    decoded_image = differential_decoding(diff_image)

    save_pgm_binary("output_binary.pgm", diff_image)