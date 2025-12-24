import numpy as np
from data_operations import *
from image_encoder import encode_image_both_methods
from image_decoder import decode_image_both_methods

if __name__ == '__main__':
    # File paths
    # original_image = "data/obrazy_testowe/lena.pgm"
    # golomb_compressed = "data/obrazy_testowe/lena_golomb.bin"
    # exp_golomb_compressed = "data/obrazy_testowe/lena_exp_golomb.bin"
    # golomb_decoded = "data/obrazy_testowe/lena_decoded_golomb.pgm"
    # exp_golomb_decoded = "data/obrazy_testowe/lena_decoded_exp_golomb.pgm"

    original_image = "data/rozklady_testowe/normal_30.pgm"
    golomb_compressed = "data/rozklady_testowe/normal_30_golomb.bin"
    exp_golomb_compressed = "data/rozklady_testowe/normal_30_exp_golomb.bin"
    golomb_decoded = "data/rozklady_testowe/normal_30_decoded_golomb.pgm"
    exp_golomb_decoded = "data/rozklady_testowe/normal_30_decoded_exp_golomb.pgm"
    #dodana linijka testowa

    # Encode
    print("=== Encoding ===")
    encode_image_both_methods(
        original_image,
        golomb_compressed,
        exp_golomb_compressed,
        golomb_m=8,
        exp_golomb_k=4
    )

    # Decode
    print("\n=== Decoding ===")
    decode_image_both_methods(
        golomb_compressed,
        exp_golomb_compressed,
        golomb_decoded,
        exp_golomb_decoded
    )

    # Verify reconstruction
    original = load_image(original_image)
    golomb_result = load_image(golomb_decoded)
    exp_golomb_result = load_image(exp_golomb_decoded)

    print("\n=== Verification ===")
    print("Golomb coding reconstruction:", "Perfect" if np.array_equal(original, golomb_result) else "Loss occurred")
    print("Exp-Golomb coding reconstruction:", "Perfect" if np.array_equal(original, exp_golomb_result) else "Loss occurred")
    print("Finished")