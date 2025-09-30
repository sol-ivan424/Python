def main(bit_fields):
    bit_offsets = {"S2": 2, "S3": 6, "S4": 8}

    result = 0
    for name, hex_value in bit_fields:
        int_value = int(hex_value, 16)
        bit_offset = bit_offsets[name]
        result |= int_value << bit_offset

    return result