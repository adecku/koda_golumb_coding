import numpy as np
import bitarray
from data_operations import differential_decoding
from exp_golomb_coder import ExpGolombCoder
from golomb_coder import GolombCoder

def decode_image(input_path, output_path, method):
    """Decode an image that was encoded with either Golomb or Exp-Golomb method"""
    # Read the binary file
    with open(input_path, 'rb') as f:
        bitstream = bitarray.bitarray()
        bitstream.fromfile(f)
    
    # First 32 bits (4 bytes) contain the parameter (m or k)
    param_bits = bitstream[:32]
    param = int.from_bytes(param_bits.tobytes(), byteorder='big')
    
    # Next 64 bits (8 bytes) contain image dimensions (height and width)
    height_bits = bitstream[32:64]
    width_bits = bitstream[64:96]
    height = int.from_bytes(height_bits.tobytes(), byteorder='big')
    width = int.from_bytes(width_bits.tobytes(), byteorder='big')
    
    # Create appropriate decoder
    if method == 'golomb':
        coder = GolombCoder(param)
    elif method == 'exp-golomb':
        coder = ExpGolombCoder(param)
    else:
        raise ValueError("Invalid method name. Use 'golomb' or 'exp-golomb'")
    
    # Convert remaining bits to string for decoding
    encoded_data = bitstream[96:].to01()
    
    # Decode the pixel values
    decoded_pixels = []
    current_pos = 0
    total_pixels = height * width
    
    while len(decoded_pixels) < total_pixels and current_pos < len(encoded_data):
        # Find the end of the current encoded value
        if method == 'golomb':
            # Find end of unary part
            end_pos = current_pos
            while end_pos < len(encoded_data) and encoded_data[end_pos] == '1':
                end_pos += 1
            end_pos += 1  # Include the '0' terminator
            
            # Calculate binary part length
            b = np.ceil(np.log2(param)).astype(int)
            cutoff = (1 << b) - param
            
            # Read enough bits to determine if r < cutoff
            temp_r = int(encoded_data[end_pos:end_pos + b - 1], 2)
            if temp_r < cutoff:
                end_pos += b - 1  # Use b-1 bits
            else:
                end_pos += b  # Use b bits
            
        else:  # exp-golomb
            # Find end of unary part
            end_pos = current_pos
            while end_pos < len(encoded_data) and encoded_data[end_pos] == '0':
                end_pos += 1
            end_pos += end_pos - current_pos + 1  # Add binary part length
        
        # Decode the value
        if end_pos <= len(encoded_data):
            value = coder.decode(encoded_data[current_pos:end_pos])
            decoded_pixels.append(value)
            current_pos = end_pos
    
    # Reshape into image array
    diff_image = np.array(decoded_pixels, dtype=np.int16).reshape((height, width))
    
    # Apply differential decoding
    decoded_image = differential_decoding(diff_image)
    
    # Convert to 8-bit format (0-255 range) for PGM compatibility
    decoded_image = np.clip(decoded_image, 0, 255).astype(np.uint8)
    
    # Save the decoded image as PGM
    with open(output_path, 'wb') as f:
        f.write(b'P5\n')  # PGM magic number
        f.write(f'{width} {height}\n'.encode())  # dimensions
        f.write(b'255\n')  # maximum value
        decoded_image.tofile(f)  # pixel data
    
    return decoded_image

def decode_image_both_methods(golomb_input, exp_golomb_input, golomb_output, exp_golomb_output):
    """Decode images that were encoded with both methods"""
    try:
        # Decode Golomb
        print("Starting Golomb decoding")
        golomb_image = decode_image(golomb_input, golomb_output, 'golomb')
        print(f"Golomb decoding completed. Output saved to {golomb_output}")
        
        # Decode Exp-Golomb
        print("Starting Exp-Golomb decoding")
        exp_golomb_image = decode_image(exp_golomb_input, exp_golomb_output, 'exp-golomb')
        print(f"Exp-Golomb decoding completed. Output saved to {exp_golomb_output}")
        
        return golomb_image, exp_golomb_image
        
    except Exception as e:
        print(f"Error during decoding: {str(e)}")
        raise

# Example usage
if __name__ == "__main__":
    decode_image_both_methods(
        "data/obrazy_testowe/mandril_golomb.bin",
        "data/obrazy_testowe/mandril_exp_golomb.bin",
        "data/obrazy_testowe/mandril_decoded_golomb.pgm",
        "data/obrazy_testowe/mandril_decoded_exp_golomb.pgm"
    )
