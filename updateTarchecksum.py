import re

HEADERSIZE=512
CHECKSUMOFFSET=148
CHECKSUMSIZE=8
MAGICOFFSET=257
MAGICSIZE=6
GIDOFFSET=0x74
MODEOFFSET=0x64

def calcChecksum(tarHeader):
    checksum = 0
    for index, b in enumerate(tarHeader):
        # byte b
        if index >= CHECKSUMOFFSET and index < CHECKSUMOFFSET+CHECKSUMSIZE:
            checksum += 32 # space

        else:
            checksum += b
    return checksum

def findTarHeaders(data):
    offsets = []
    for blockOffset in range(0, len(data), 512):
        if data[blockOffset+MAGICOFFSET:blockOffset+MAGICOFFSET+MAGICSIZE] == b'ustar ':
            offsets.append(blockOffset)
    return offsets

def modify(data, offset, new):
    return data[:offset] + new + data[offset+len(new):]

def patchChecksum(data, offset):
    print('[+] Update CHECKSUM block->', data[offset:offset+100].decode('utf8'))
    checksum = calcChecksum(data[offset:offset+HEADERSIZE])
    print(' '*8, data[offset+CHECKSUMOFFSET:offset+CHECKSUMOFFSET+CHECKSUMSIZE], '->', '{:06o}\x00\x20'.format(checksum).encode('utf8'))
    data = modify(data, offset+CHECKSUMOFFSET, '{:06o}\x00\x20'.format(checksum).encode('utf8'))
    return data


def generateLonglinkBlock(name):
    size = '{:011o}\x00'.format(len(name)).encode('utf8')
    header = bytearray(512)
    header = modify(header, 0, b'././@LongLink')
    header = modify(header, MAGICOFFSET, b'ustar  ')
    header = modify(header, 0x6c, b'0000000')
    header = modify(header, 0x74, b'0000000')
    header = modify(header, 0x7c, size)
    header = modify(header, 0x88, b'00000000000')
    header = modify(header, 0x9c, b'L')
    header = modify(header, 0x107, b'\x20\x00')
    header = modify(header, 0x109, b'root')
    header = modify(header, 0x129, b'root')

    data = bytearray(512)
    data = modify(data, 0, name)
    return header + data


def patchLocation(data, offset, prefix, match):
    if data[offset] == 0:
        return data, offset
    s = b''

    for length in range(100):
        if data[offset+length] == 0:
            s = data[offset:offset+length]
            break
    assert(s != b'')

    if re.search(match, s) == None:
        return data, offset

    print(f'[+] CHANGE FILENAME {s} -> {prefix + s}')

    if len(prefix + s) < 100:
        data = modify(data, offset, prefix + s)
    else:
        print('[.] filename is too long, add longlinking block')
        longlinkBlock = generateLonglinkBlock(prefix+s)
        # insertion
        data = modify(data, offset, longlinkBlock + data[offset:])
        print(len(data), offset, len(longlinkBlock))
        offset = offset + len(longlinkBlock)
    return data, offset


def patchGid(data, offset, gid):
    print('[+] Update GID block->', data[offset:offset+100].decode('utf8'))
    print(' '*8,data[offset+GIDOFFSET:offset+GIDOFFSET+8], '->', '{:07o}\x00'.format(gid).encode('utf8'))
    data = modify(data, offset+GIDOFFSET, '{:07o}\x00'.format(gid).encode('utf8'))
    return data

def patchMod(data, offset, mode):
    print('[+] Update Mode block->', data[offset:offset+100].decode('utf8'))
    print(' '*8, data[offset+MODEOFFSET:offset+MODEOFFSET+8], '->', '{:07o}\x00'.format(mode).encode('utf8'))
    data = modify(data, offset+MODEOFFSET, '{:07o}\x00'.format(mode).encode('utf8'))
    return data

def main(filename = 'com.example.android.notepad/test.tar', prefix = '', match='.*', gid = '', mode=''):
    data = open(filename, 'rb').read()

    if prefix != '' :
        offset = 0
        while offset < len(data):
            if data[offset+MAGICOFFSET:offset+MAGICOFFSET+MAGICSIZE] == b'ustar ':
                data, offset = patchLocation(data, offset, prefix.encode('utf8'), match)
            offset += 512

    for offset in findTarHeaders(data):
        if re.search(match, data[offset:offset+100]) == None:
            continue

        if gid != '' :
            data = patchGid(data, offset, int(gid))
        if mode != '':
            data = patchMod(data, offset, int(mode, 8))
        data = patchChecksum(data, offset)
        print()
    with open(filename, 'wb') as f:
        f.write(data)


if __name__ == "__main__":
    import sys
    main(filename=sys.argv[1], match=sys.argv[2].encode('utf8'), prefix=sys.argv[3], mode=sys.argv[4])
