def from_string_data(b: bytes) -> tuple[str, int]:
    """
    Convert bytes from osu! String data type to utf8

    https://osu.ppy.sh/wiki/en/Client/File_formats/Osr_%28file_format%29#data-types

    :param b:
    :return: tuple(utf8 string, offset)
    """
    if b[0] == 11:
        uleb128_len = seek_uleb128(b[1:])
        data_offset = 1 + uleb128_len
        data_len = from_uleb128(b[1:data_offset])
        end_offset = data_offset + data_len
        data = b[data_offset:end_offset].decode("utf-8")
        return (data, end_offset)
    else:
        raise NotImplementedError


def to_uleb128(d: int) -> bytes:
    """
    Encode unsigned numbers to ULEB128

    Input an unsigned number to encode.

    Output bytes of the encoded unsigned number, LSB to MSB
    """

    """
    How does it work ?

    It use bitwise operation to encode every packs of 7 bits:
        First we apply a right bitshift to move the pack of 7 bits we need to look at to the end.
        Then we use a mask of 0x7f and a bitwise AND between 0x80 to add a leading "1" to our 7 bits.
        We save the newly created byte in a list and repeat the previous steps for every packs of 7 bits.
        When we are done looking at every packs we change the first bit of the MSB to a "0",
        this is done with a bitwise AND between 0x7f.
        The list is then converted to a bytes object and outputed from LSB to MSB

    The hardest part is to find "r" the value of the applied right bitshift.
    How to easily find "r":
        First we need to find "l" the bitlength of our input bytes.
        Then we do `r = l // 8 + 1` to find the number of bytes needed to fully represent our input.
        To account for case where two bitshift are needed for a single byte we add (l - 1) // 49 to "r" ex: input >= 2^50 or 2^99 ... 
    """

    l = d.bit_length()
    r = (l // 8 + 1) + (l - 1) // 49

    dl = []
    for i in range(r):
        dl.append((d >> i * 7) & 0x7f | 0x80)
    dl[-1] = dl[-1] & 0x7f
    return bytes(dl)


def from_uleb128(b: bytes) -> int:
    """
    Decode ULEB128 to bytes (LSB -> MSB)

    Works by doing a bitwise AND with a mask of 0x7f on every bytes

    https://en.wikipedia.org/wiki/LEB128#Unsigned_LEB128

    Output bytes values in base10
    """
    output = 0
    for index, byte in enumerate(list(b)):
        output = (byte & 0x7f) << index*7 | output
    return output


def seek_uleb128(b: bytes) -> int:
    """
    seek the length in byte of an uleb128

    input bytes (LSB to MSB)

    output uleb128 length in bytes
    """
    end_loc = None
    byte_index = 0
    for byte in list(b):
        if byte < 128:
            end_loc = byte_index + 1
            break
        byte_index += 1
    if end_loc == None: raise ValueError("Could not find uleb128 end")
    return end_loc
