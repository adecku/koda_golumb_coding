import math

# Trzeba dodać zigzag coding dla wartości ujemnych po kodowaniu różnicowym
class GolombCoder:
    def __init__(self, m):
        self.m = m

    def encode(self, num):
        # Cześć unarna
        q = num // self.m
        # Cześć binarna
        r = num % self.m

        # Kodowanie wartości unarnej
        unary_part = '1' * q + '0'

        # Obliczanie ilości bitów dla części binarnej
        b = math.ceil(math.log2(self.m))
        # Obliczanie dla jakich wartości możemy uzyć mniejszej ilości bitów
        # (1 << b) == (1 ** b), różnica polega na wydajności
        cutoff = (1 << b) - self.m

        # Kodowanie wartości binarnej
        if r < cutoff:
            binary_part = f"{r:0{b - 1}b}"
        else:
            binary_part = f"{r + cutoff:0{b}b}"

        return unary_part + binary_part


    def decode(self, code):
        q = 0
        i = 0
        while code[i] == '1':
            q += 1
            i += 1
        # i wskazuje na '0' -> koniec zapisu unarnego -> pomijamy
        i += 1

        b = math.ceil(math.log2(self.m))
        cutoff = (1 << b) - self.m

        if int(code[i:i + b - 1], 2) < cutoff:
            # Konwersja bitów na liczbę dziesiętną
            r = int(code[i:i + b - 1], 2)
        else:
            # Konwersja bitów na liczbę dziesiętną
            r = int(code[i:i + b], 2) - cutoff

        return q * self.m + r
