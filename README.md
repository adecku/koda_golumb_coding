# Golomb and Exponential Golomb Coding Implementation

This project implements Golomb coding and Exponential Golomb coding algorithms, along with testing functionality for various data distributions and image compression.

## Features

- Golomb coding with configurable parameter m
- Exponential Golomb coding with configurable order k
- Testing with different probability distributions:
  - Uniform
  - Normal
  - Geometric
  - Laplace
- Image compression testing using differential encoding
- Entropy calculation and compression efficiency analysis

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the test script to evaluate coding performance on synthetic data:
```bash
python src/test_golomb.py
```

### Testing with Images

To test with your own images, modify the `test_image_coding()` call in `src/test_golomb.py`:
```python
test_image_coding("path/to/your/image.png")
```

### Custom Testing

You can also use the coding classes directly:

```python
from src.golomb_coding import GolombCoder, ExpGolombCoder

# Golomb coding
golomb = GolombCoder(m=4)
encoded = golomb.encode_number(42)
decoded = golomb.decode_number(encoded)

# Exponential Golomb coding
exp_golomb = ExpGolombCoder(k=1)
encoded = exp_golomb.encode_number(42)
decoded = exp_golomb.decode_number(encoded)
```

## Code Structure

- `src/golomb_coding.py`: Core implementation of Golomb and Exp-Golomb coding
- `src/data_operations.py`: Image loading and differential encoding operations
- `src/test_golomb.py`: Testing and evaluation functionality

## Analysis Features

- Distribution visualization with histograms
- Entropy calculation
- Average code length calculation
- Compression efficiency comparison 