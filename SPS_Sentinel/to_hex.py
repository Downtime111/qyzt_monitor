def str_to_hex(s):
    return ' '.join([hex(ord(c)).replace('0x', '') for c in s])


def hex_to_str(s):
    return ''.join([chr(i) for i in [int(b, 16) for b in s.split(' ')]])


def str_to_bin(s):
    return ' '.join([bin(ord(c)).replace('0b', '') for c in s])


def bin_to_str(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])


if __name__ == '__main__':
    print(str_to_hex("export 0 20210816 20210816"))
    print(hex_to_str("65 78 70 6f 72 74 20 30 20 32 30 32 31 30 38 31 36 20 32 30 32 31 30 38 31 36"))
    print(str_to_bin("export 0 20210816 20210816"))
    print(bin_to_str("1100101 1111000 1110000 1101111 1110010 1110100 100000 110000 100000 110010 110000 110010 110001 110000 111000 110001 110110 100000 110010 110000 110010 110001 110000 111000 110001 110110"))