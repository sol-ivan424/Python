import struct


def read_structure_A(data, offset):
    a_uint32, = struct.unpack_from("<I", data, offset)
    offset += 4
    b_struct, offset = read_structure_B(data, offset)
    a_uint8_1, = struct.unpack_from("<B", data, offset)
    offset += 1
    a_uint8_2, = struct.unpack_from("<B", data, offset)
    offset += 1
    return {
        "A1": a_uint32,
        "A2": b_struct,
        "A3": a_uint8_1,
        "A4": a_uint8_2
    }, offset


def read_structure_B(data, offset):
    b_float, = struct.unpack_from("<f", data, offset)
    offset += 4
    b_array_size_c, b_array_address_c = struct.unpack_from("<II", data, offset)
    offset += 8
    b_array_size_f, b_array_address_f = struct.unpack_from("<IH", data, offset)
    offset += 6
    b_int8_1, = struct.unpack_from("<b", data, offset)
    offset += 1
    b_float_2, = struct.unpack_from("<f", data, offset)
    offset += 4
    b_array_int8 = struct.unpack_from("<3b", data, offset)
    offset += 3
    b_address_f, = struct.unpack_from("<I", data, offset)
    offset += 4
    b_address_g, = struct.unpack_from("<I", data, offset)
    offset += 4

    # Read array of addresses for structures C
    c_addresses = []
    for i in range(b_array_size_c):
        c_address, = struct.unpack_from("<I", data, b_array_address_c+i*4)
        c_addresses.append(c_address)
    c_structs = [read_structure_C(data, addr)[0] for addr in c_addresses]

    # Read array of floats
    float_array = []
    for i in range(b_array_size_f):
        float_value, = struct.unpack_from("<f", data, b_array_address_f+i*4)
        float_array.append(float_value)

    # Read structure F and G
    f_struct = read_structure_F(data, b_address_f)[0]
    g_struct = read_structure_G(data, b_address_g)[0]

    return {
        "B1": b_float,
        "B2": c_structs,
        "B3": float_array,
        "B4": b_int8_1,
        "B5": b_float_2,
        "B6": list(b_array_int8),
        "B7": f_struct,
        "B8": g_struct,
    }, offset


def read_structure_C(data, offset):
    c_int32, = struct.unpack_from("<i", data, offset)
    offset += 4
    d_struct, offset = read_structure_D(data, offset)
    e_address, = struct.unpack_from("<H", data, offset)
    offset += 2
    e_struct, _ = read_structure_E(data, e_address)
    return {
        "C1": c_int32,
        "C2": d_struct,
        "C3": e_struct
    }, offset


def read_structure_D(data, offset):
    d_uint8, = struct.unpack_from("<B", data, offset)
    offset += 1
    d_int16, = struct.unpack_from("<h", data, offset)
    offset += 2
    d_int8, = struct.unpack_from("<b", data, offset)
    offset += 1
    return {
        "D1": d_uint8,
        "D2": d_int16,
        "D3": d_int8
    }, offset


def read_structure_E(data, offset):
    e_uint32, = struct.unpack_from("<I", data, offset)
    offset += 4
    e_uint16, = struct.unpack_from("<H", data, offset)
    offset += 2
    e_float, = struct.unpack_from("<f", data, offset)
    offset += 4
    e_array_uint8 = struct.unpack_from("<2B", data, offset)
    offset += 2
    return {
        "E1": e_uint32,
        "E2": e_uint16,
        "E3": e_float,
        "E4": list(e_array_uint8),
    }, offset


def read_structure_F(data, offset):
    f_uint32, = struct.unpack_from("<I", data, offset)
    offset += 4
    f_uint16_1, = struct.unpack_from("<H", data, offset)
    offset += 2
    f_array_float = struct.unpack_from("<8f", data, offset)
    offset += 32
    f_uint16_2, = struct.unpack_from("<H", data, offset)
    offset += 2
    f_int8_1, = struct.unpack_from("<b", data, offset)
    offset += 1
    f_int8_2, = struct.unpack_from("<b", data, offset)
    offset += 1
    return {
        "F1": f_uint32,
        "F2": f_uint16_1,
        "F3": list(f_array_float),
        "F4": f_uint16_2,
        "F5": f_int8_1,
        "F6": f_int8_2,
    }, offset


def read_structure_G(data, offset):
    g_uint64, = struct.unpack_from("<Q", data, offset)
    offset += 8
    g_int16, = struct.unpack_from("<h", data, offset)
    offset += 2
    g_int8, = struct.unpack_from("<b", data, offset)
    offset += 1
    return {
        "G1": g_uint64,
        "G2": g_int16,
        "G3": g_int8
    }, offset


def main(data):
    # Check signature
    signature = data[:5]
    if signature != b"\xf6JNAF":
        raise ValueError("Invalid file signature")

    # Read structure A starting from byte 5
    offset = 5
    structure_A, _ = read_structure_A(data, offset)

    return structure_A
