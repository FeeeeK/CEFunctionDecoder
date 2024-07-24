# Cheat Engine encodeFunction decoder

Originally created to decode Hexinton's Elden Ring cheat table, but can be used for any cheat table that uses `decodeFunction`.

## Usage

1. Open the cheat table in any text editor.
2. Copy first argument of `decodeFunction` (the encoded string).
3. Run `python decode_function.py` and paste the encoded string, decoded Lua bytecode will be saved to `decoded.luac`.

> [!IMPORTANT]
> Some terminals may break the string and you will get an error from zlib, in this case, save the string to a file and run `python decode_function.py < file.txt`

You can use [luadec](https://github.com/viruscamp/luadec) to decompile this bytecode.
> [!TIP]
> [This fork of luadec](https://github.com/zhangjiequan/luadec) is recommended, as it has some improvements over the original.

### For Hexinton's Elden Ring cheat table

 1. Same as above, but run `python hexinton_table_decoder.py` instead.
