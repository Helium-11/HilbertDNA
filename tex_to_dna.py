# -----------------------------
# 2-bit DNA mapping
# -----------------------------

BIT_TO_DNA = {
    "00": "A",
    "01": "T",
    "10": "G",
    "11": "C"
}

DNA_TO_BIT = {v: k for k, v in BIT_TO_DNA.items()}


# -----------------------------
# BINARY → DNA
# -----------------------------

def binary_to_dna(binary_string: str) -> str:
    dna = ""
    for i in range(0, len(binary_string), 2):
        pair = binary_string[i:i+2]
        if pair not in BIT_TO_DNA:
            raise ValueError(f"Invalid binary pair: {pair}")
        dna += BIT_TO_DNA[pair]
    return dna


def text_to_binary(text: str) -> str:
    data = text.encode("utf-8")  # convert to bytes safely

    length_header = format(len(data), "032b")

    binary_string = "".join(format(byte, "08b") for byte in data)

    full_binary = length_header + binary_string

    if len(full_binary) % 2 != 0:
        full_binary += "0"

    return full_binary


def binary_to_text(binary_string: str) -> str:

    if len(binary_string) < 32:
        raise ValueError("Binary data too short to contain length header.")

    length_bits = binary_string[:32]
    byte_length = int(length_bits, 2)

    data_bits = binary_string[32:]
    expected_bits = byte_length * 8

    if len(data_bits) < expected_bits:
        raise ValueError("Binary data shorter than expected message length.")

    bytes_list = []

    for i in range(0, expected_bits, 8):
        byte = data_bits[i:i+8]
        bytes_list.append(int(byte, 2))

    return bytes(bytes_list).decode("utf-8")





# -----------------------------
# DNA → BINARY
# -----------------------------

def dna_to_binary(dna_string: str) -> str:
    binary = ""
    dna_string = dna_string.upper()

    for base in dna_string:
        if base not in DNA_TO_BIT:
            raise ValueError(f"Invalid DNA base detected: {base}")
        binary += DNA_TO_BIT[base]

    return binary


# -----------------------------
# PUBLIC API FUNCTIONS
# -----------------------------

def text_to_dna(text: str) -> str:
    """
    Full pipeline:
    TEXT → BINARY (with parity) → DNA
    """
    binary = text_to_binary(text)
    return binary_to_dna(binary)


def dna_to_text(dna: str) -> str:
    """
    Full pipeline:
    DNA → BINARY → TEXT (with parity check)
    Raises error if parity mismatch detected.
    """
    binary = dna_to_binary(dna)
    text= binary_to_text(binary)


    return text

