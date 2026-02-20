
import numpy as np
from PIL import Image
import struct
import math


class HilbertDNACodec:
    """
    Production-ready reversible DNA <-> Image codec
    using Hilbert space-filling curve.
    """

    def __init__(self):

        self.base_to_bits = {
            'A': 0b00,
            'T': 0b01,
            'C': 0b10,
            'G': 0b11
        }

        self.bits_to_base = {v: k for k, v in self.base_to_bits.items()}

    # =====================================================
    # Hilbert Utilities (integer-only)
    # =====================================================

    def _rot(self, n, x, y, rx, ry):
        if ry == 0:
            if rx == 1:
                x = n - 1 - x
                y = n - 1 - y
            x, y = y, x
        return x, y

    def hilbert_index_to_xy(self, n, d):

        x = y = 0
        t = d
        s = 1

        while s < n:
            rx = 1 & (t // 2)
            ry = 1 & (t ^ rx)
            x, y = self._rot(s, x, y, rx, ry)
            x += s * rx
            y += s * ry
            t //= 4
            s *= 2

        return x, y

    # =====================================================
    # ENCODING
    # =====================================================

    def dna_to_image(self, dna_sequence, output_path="hilbert_dna.png"):

        if not dna_sequence:
            raise ValueError("DNA sequence cannot be empty")

        if not all(b in "ATCG" for b in dna_sequence):
            raise ValueError("DNA must contain only A,T,C,G")

        # ---- Pack DNA ----
        original_length = len(dna_sequence)
        header = struct.pack(">I", original_length)

        dna_bytes = bytearray()

        for i in range(0, len(dna_sequence), 2):
            b1 = self.base_to_bits[dna_sequence[i]]
            b2 = self.base_to_bits[dna_sequence[i + 1]] if i + 1 < len(dna_sequence) else 0
            packed = (b1 << 2) | b2
            dna_bytes.append(packed)

        payload = header + dna_bytes
        total_bytes = len(payload)

        # ---- Determine Hilbert grid size ----
        side = 1
        while side * side < total_bytes:
            side *= 2

        grid = np.zeros((side, side, 3), dtype=np.uint8)

        # ---- Fill Hilbert coordinates ----
        for idx in range(total_bytes):

            x, y = self.hilbert_index_to_xy(side, idx)

            byte = payload[idx]

            r = byte

            # decorative channels (safe)
            g = (byte * 73) % 256
            b = (byte * 151) % 256

            grid[y, x] = [r, g, b]

        img = Image.fromarray(grid, "RGB")
        img.save(output_path)

        return img


    # =====================================================
    # DECODING
    # =====================================================

    def image_to_dna(self, image_path):

        img = Image.open(image_path)
        grid = np.array(img)

        side = grid.shape[0]  # full square

        payload = []

        for idx in range(side * side):

            x, y = self.hilbert_index_to_xy(side, idx)
            r= grid[y, x][0]
            payload.append(r)

        payload = bytes(payload)

    # Extract header
        original_length = struct.unpack(">I", payload[:4])[0]

        dna_bytes_needed = math.ceil(original_length / 2)

        dna_bytes = payload[4:4 + dna_bytes_needed]

        dna_sequence = []

        for byte in dna_bytes:
            b1 = (byte >> 2) & 0b11
            b2 = byte & 0b11

            dna_sequence.append(self.bits_to_base[b1])
            dna_sequence.append(self.bits_to_base[b2])

        return "".join(dna_sequence[:original_length])


# =====================================================
# CLI test
# =====================================================

if __name__ == "__main__":

    import random

    bases = ['A', 'T', 'C', 'G']
    dna = ""

    codec = HilbertDNACodec()

    codec.dna_to_image(dna, "test.png")
    decoded = codec.image_to_dna("test.png")
    print(decoded)

    print("Match:", dna == decoded)