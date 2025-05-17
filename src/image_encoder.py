import numpy as np
import bitarray
import bitarray.util
from data_operations import load_image, differential_encoding, differential_decoding
from exp_golomb_coder import ExpGolombCoder
from golomb_coder import GolombCoder


def encode_image(image_path, output_path, method, param):
    """Encode image using a single method (Golomb or Exp-Golomb)"""
    image = load_image(image_path)
    diff_image = differential_encoding(image)
    bitstream = bitarray.bitarray()

    if method == 'golomb':
        coder = GolombCoder(param)
    elif method == 'exp-golomb':
        coder = ExpGolombCoder(param)
    else:
        raise ValueError("Invalid method name. Use 'golomb' or 'exp-golomb'")

    # Store the encoding parameters at the start of the file
    # This will help during decoding
    param_bits = bitarray.bitarray()
    param_bits.frombytes(param.to_bytes(4, byteorder='big'))
    bitstream.extend(param_bits)

    # Store image dimensions for reconstruction
    height, width = diff_image.shape
    dim_bits = bitarray.bitarray()
    dim_bits.frombytes(height.to_bytes(4, byteorder='big'))
    dim_bits.frombytes(width.to_bytes(4, byteorder='big'))
    bitstream.extend(dim_bits)

    for row in diff_image:
        for pixel in row:
            encoded_pixel = coder.encode(pixel)
            bitstream.extend(bitarray.bitarray(encoded_pixel))

    # Write binary data directly
    with open(output_path, "wb") as f:
        bitstream.tofile(f)
    
    return bitstream


def encode_image_both_methods(image_path, golomb_output_path, exp_golomb_output_path, golomb_m, exp_golomb_k):
    """Encode image using both Golomb and Exp-Golomb methods"""
    try:
        # Get original file size for comparison
        image = load_image(image_path)
        original_size = image.size * image.itemsize * 8  # size in bits
        
        # Encode with Golomb
        print("Starting Golomb encoding with m =", golomb_m)
        golomb_bitstream = encode_image(image_path, golomb_output_path, 'golomb', golomb_m)
        print(f"Golomb encoding completed. Output saved to {golomb_output_path}")
        golomb_size = len(golomb_bitstream)
        
        # Encode with Exp-Golomb
        print("Starting Exp-Golomb encoding with k =", exp_golomb_k)
        exp_golomb_bitstream = encode_image(image_path, exp_golomb_output_path, 'exp-golomb', exp_golomb_k)
        print(f"Exp-Golomb encoding completed. Output saved to {exp_golomb_output_path}")
        exp_golomb_size = len(exp_golomb_bitstream)
        
        # Print compression statistics
        print("\nCompression Statistics:")
        print(f"Original image size: {original_size} bits")
        print(f"Golomb encoded size: {golomb_size} bits (ratio: {original_size/golomb_size:.2f}x)")
        print(f"Exp-Golomb encoded size: {exp_golomb_size} bits (ratio: {original_size/exp_golomb_size:.2f}x)")
        
        return golomb_bitstream, exp_golomb_bitstream
        
    except Exception as e:
        print(f"Error during encoding: {str(e)}")
        raise

# Example usage
if __name__ == "__main__":
    encode_image_both_methods(
        "../data/obrazy_testowe/mandril.pgm",
        "../data/obrazy_testowe/mandril_golomb.bin",  # Changed extension to .bin
        "../data/obrazy_testowe/mandril_exp_golomb.bin",  # Changed extension to .bin
        golomb_m=4,  # Golomb parameter
        exp_golomb_k=0  # Exp-Golomb parameter
    )
