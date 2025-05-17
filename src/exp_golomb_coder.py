class ExpGolombCoder:
    def __init__(self, k):
        # przesunięcie liczby -> k większe dla większych liczb
        self.k = k

    def zigzag_encode(self, num):
        return (num << 1) ^ (num >> 31)

    def zigzag_decode(self, num):
        return (num >> 1) ^ -(num & 1)

    def encode(self, num):
        # Convert numpy integer to Python integer
        num = int(num)
        num = self.zigzag_encode(num)
        # Dodajemy przesunięcie o 1 bit
        num += (1 << self.k)
        b = num.bit_length()
        # część unarna
        unary_part = '0' * (b - 1)
        # część binarna
        binary_part = f"{num:0{b}b}"
        return unary_part + binary_part

    def decode(self, code):
        i = 0
        while code[i] == '0':
            i += 1

        length = i + 1
        value = int(code[i:i + length], 2) - (1 << self.k)

        return self.zigzag_decode(value)