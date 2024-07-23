import io
import zlib


class CustomBase85:
    custom_base85 = (
        "0123456789"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz"
        "!#$%()*+,-./:;=?@[]^_{}"
    )
    powers_of_85 = (52200625, 614125, 7225, 85, 1)

    @staticmethod
    def base85_to_bin(input_string_base85):
        result = bytearray()
        size = len(input_string_base85)
        for i in range(0, size, 5):
            chunk = input_string_base85[i : i + 5]
            a = 0
            for j, char in enumerate(chunk):
                index = CustomBase85.custom_base85.find(char)
                if index == -1:
                    msg = f"Invalid character '{char}' in input."
                    raise ValueError(msg)
                a += index * CustomBase85.powers_of_85[j]
            if len(chunk) == 5:  # noqa: PLR2004
                result.extend(a.to_bytes(4, "big"))
                continue
            remainder = size % 5
            if remainder in (2, 3, 4):
                padding = 84 + CustomBase85.powers_of_85[remainder - 1]
                a += padding
                result.extend(a.to_bytes(4, "big")[: remainder - 1])
        return result


def lua_decode_function(encoded_str) -> io.BytesIO:
    decoded_bytes = CustomBase85.base85_to_bin(encoded_str)
    decompressed_fileio = io.BytesIO(zlib.decompress(decoded_bytes))
    return decompressed_fileio


def read_bytes(f, length: int) -> bytes:
    data = f.read(length)
    if len(data) != length:
        raise EOFError
    return data


def read_u8(f) -> int:
    return read_bytes(f, 1)[0]


def read_string(file):
    size = int.from_bytes(file.read(1))
    if size == 0:
        return ""
    size -= 1  # size includes null terminator
    return file.read(size).decode("utf-8")


def read_long_string(file):
    read_bytes(file, 1)  # skip 0xFF byte
    size_b = read_bytes(file, 8)
    size = int.from_bytes(size_b, "little")
    if size == 0:
        return ""
    size -= 1  # size includes null terminator
    return file.read(size).decode("utf-8")


def read_constants(file):
    constants = []
    num_constants = read_bytes(file, 4)
    num_constants = int.from_bytes(num_constants, "little")
    for _ in range(num_constants):
        const_type = int.from_bytes(file.read(1))
        if const_type == 0x04:  # noqa: PLR2004
            string = read_string(file)
            constants.append(string)
        elif const_type == 0x14:  # noqa: PLR2004
            string = read_long_string(file)
            constants.append(string)
        elif const_type == 0x13:  # noqa: PLR2004
            number_b = read_bytes(file, 8)
            number = int.from_bytes(number_b, "little")
            constants.append(number)
    return constants


def extract_constants_from_luac(fileobj: io.BytesIO):
    fileobj.seek(0)
    # validate the header
    header = read_bytes(fileobj, 5)
    if header != b"\x1bLua\x53":
        msg = "Invalid Lua bytecode header"
        raise ValueError(msg)
    # skip format version
    read_bytes(fileobj, 1)
    signature = read_bytes(fileobj, 6)
    if signature != b"\x19\x93\r\n\x1a\n":
        msg = "Invalid Lua signature"
        raise ValueError(msg)
    sizes = read_bytes(fileobj, 5)
    # 4 bytes for int, 8 bytes for size_t, 4 bytes for instruction, 8 bytes for lua_Integer, 8 bytes for lua_Number
    if sizes != b"\x04\x08\x04\x08\x08":
        msg = "Invalid Lua sizes"
        raise ValueError
    endianess = read_bytes(fileobj, 8)
    # 0x5678 in little endian
    if endianess != b"\x78\x56\x00\x00\x00\x00\x00\x00":
        msg = "Invalid Lua endianess"
        raise ValueError(msg)
    float_header = read_bytes(fileobj, 8)
    # 370.5
    if float_header != b"\x00\x00\x00\x00\x00\x28\x77\x40":
        msg = "Invalid Lua float header"
        raise ValueError(msg)
    # skip upvalue info
    read_bytes(fileobj, 1)
    # source name
    read_string(fileobj)
    # skip line info
    read_bytes(fileobj, 4)
    # skip last line defined
    read_bytes(fileobj, 4)
    # number of parameters
    read_bytes(fileobj, 1)
    # is_vararg
    read_bytes(fileobj, 1)
    # max stack size
    read_bytes(fileobj, 1)
    # number of instructions
    code_size_b = read_bytes(fileobj, 4)
    code_size = int.from_bytes(code_size_b, "little")
    # skip instructions
    read_bytes(fileobj, code_size * 4)

    constants = read_constants(fileobj)
    return constants


if __name__ == "__main__":
    encoded_str = input("Enter the encoded string: ")
    lua_bytecode = lua_decode_function(encoded_str)
    with open("decoded.luac", "wb") as f:
        f.write(lua_bytecode.read())
