import math

class GolombCoder:
    def __init__(self, m):
        self.m = m

    def zigzag_encode(self, num):
        return (num << 1) ^ (num >> 31)

    def zigzag_decode(self, num):
        return (num >> 1) ^ -(num & 1)

    def encode(self, num):
        num = self.zigzag_encode(num)
        # Unary part
        q = num // self.m
        # Binary part
        r = num % self.m

        # Encoding unary value
        unary_part = '1' * q + '0'

        # Calculating number of bits for binary part
        b = math.ceil(math.log2(self.m))
        # Calculating for which values we can use fewer bits
        # (1 << b) == (1 ** b), the difference is in efficiency
        cutoff = (1 << b) - self.m

        # Encoding binary value
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
        # i points to '0' -> end of unary encoding -> skip it
        i += 1

        b = math.ceil(math.log2(self.m))
        cutoff = (1 << b) - self.m

        if int(code[i:i + b - 1], 2) < cutoff:
            # Converting bits to decimal number
            r = int(code[i:i + b - 1], 2)
        else:
            # Converting bits to decimal number
            r = int(code[i:i + b], 2) - cutoff

        num = q * self.m + r

        return self.zigzag_decode(num)