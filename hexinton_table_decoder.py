from decode_function import extract_constants_from_luac, lua_decode_function


def decode_function(encoded_string, some_constant):
    def greatest_common_divisor(num1, num2):
        while num2 != 0:
            z = num1
            num1 = num2
            num2 = z % num2
        return num1

    encoded_str_len = len(encoded_string)
    some_constant = round(
        some_constant / greatest_common_divisor(some_constant, encoded_str_len) % encoded_str_len
    )
    l_0_16 = (encoded_str_len // 2 + some_constant) % encoded_str_len
    chr_dict = {}
    result_str = ""
    l_0_19 = 33
    l_0_20 = 126

    for i in range(1, encoded_str_len + 1):
        l_0_25 = 1 + (i * some_constant + l_0_16) % encoded_str_len
        l_0_37 = ord(encoded_string[i - 1])
        chr_dict[l_0_25] = l_0_37
        if l_0_19 <= l_0_37 <= l_0_20:
            l_0_37 = (l_0_37 - l_0_19 + some_constant * (i % (l_0_20 + 1 - l_0_19)) - i) % (
                l_0_20 + 1 - l_0_19
            ) + l_0_19
            chr_dict[l_0_25] = l_0_37

    for i in range(1, encoded_str_len + 1):
        result_str += chr(chr_dict[i])

    return lua_decode_function(result_str)


if __name__ == "__main__":
    encoded_str = input("Enter the encoded string: ")
    first_pass_lua_bytecode = lua_decode_function(encoded_str)
    # check for decodeFunction call in the bytecode
    first_pass_constants = extract_constants_from_luac(first_pass_lua_bytecode)
    if "decodeFunction" not in first_pass_constants:
        print("Encoded string was just result of encodeFunction without obfuscation")  # noqa: T201
        print("Saving the bytecode to decoded.luac")  # noqa: T201
        with open("decoded.luac", "wb") as f:
            f.write(first_pass_lua_bytecode.read())
    else:
        constants = extract_constants_from_luac(first_pass_lua_bytecode)
        obfuscated_string = constants[-2]
        SOME_RANDOM_CONSTANT = constants[-1]
        second_pass_lua_bytecode = decode_function(obfuscated_string, SOME_RANDOM_CONSTANT)
        print("Saving the bytecode to decoded.luac")  # noqa: T201
        with open("decoded.luac", "wb") as f:
            f.write(second_pass_lua_bytecode.read())
