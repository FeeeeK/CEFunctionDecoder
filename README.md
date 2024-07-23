# Cheat Engine encodeFunction decoder

Originally created to decode Hexinton's Elden Ring cheat table, but can be used for any cheat table that uses `decodeFunction`.

## Usage

1. Open the cheat table in any text editor.
2. Copy first argument of `decodeFunction` (the encoded string).
3. Run `python decode_function.py` and paste the encoded string.
4. Decoded Lua bytecode will be saved to `decoded.luac`.

You can use [luadec](https://github.com/viruscamp/luadec) to decompile this bytecode.

### For Hexinton's Elden Ring cheat table

 1. Same as above, but run `python hexinton_table_decoder.py` instead.
