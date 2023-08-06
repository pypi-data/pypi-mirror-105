#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Decompressione immagini bitmap utilizzate da Mdf3"""
# Ispirato a:
# http://pseentertainmentcorp.com/smf/index.php?topic=2034.0
import struct
from .csutil import BytesIO

bitmapHeader_fmt = '<BBLHHLLLLHHLLLLLL'
bitmapHeader_len = struct.calcsize(bitmapHeader_fmt)

colormap_fmt = '<'
colormap_bin = b''
for i in range(256):
    colormap_fmt += 'BBBB'
    colormap_bin += struct.pack('<BBBB', i,i,i,i)
#colormap_fmt = '<' + 'I' * 256
colormap_len = struct.calcsize(colormap_fmt)
#colormap_bin = struct.pack(colormap_fmt, *tuple(range(0, 256)))
# Coppie Colore, Conteggio compresse
inbit_fmt = '<BB'
inbit_len = struct.calcsize(inbit_fmt)
# Colori decompressi
outbit_fmt = '<B'
outbit_len = struct.calcsize(outbit_fmt)
# Bitmap header positions
MN1 = 0
MN2 = 1
FILESIZE = 2
UNDEF1 = 3
UNDEF2 = 4
OFFSET = 5
HEADERLENGTH = 6
WIDTH = 7
HEIGHT = 8
COLORPLANES = 9
COLORDEPTH = 10
COMPRESSION = 11
IMAGESIZE = 12
HRES = 13
VRES = 14
PALETTE = 15
IMPORTANTCOLORS = 16

outHeader = [66,  # mn1
             77,  # mn2
             0,  # filesize
             0,  # u1
             0,  # u2
             54,  # offset
             40,  # hl
             640,  # w
             480,  # h
             1,  # cp
             8,  # cd
             0,  # compress
             0,  # imgsize
             0,  # hres
             0,  # vres
             256,  # palette
             0]  # impc


def decompress_bitmap(img):
    img.seek(0)
    # Leggo header
    fh = struct.unpack(bitmapHeader_fmt, img.read(bitmapHeader_len))
    outH = list(outHeader[:])
    for val in WIDTH, HEIGHT:
        outH[val] = fh[val]
    # Leggo la mappa dei colori
    cmap = img.read(colormap_len)
    out = b''
    while True:
        r = img.read(inbit_len)
        if len(r) != inbit_len:
            break
        n, c = struct.unpack(inbit_fmt, r)
        out += struct.pack(outbit_fmt, c) * n

    outH[IMAGESIZE] = len(out)
    outH[OFFSET] = bitmapHeader_len + colormap_len
    outH[FILESIZE] = outH[IMAGESIZE] + outH[OFFSET]
    out = struct.pack(bitmapHeader_fmt, *tuple(outH)) + cmap + out
    return out


def decompress(img):
    if img[:2] not in (b'IM', b'MI'):  # MI is an old id
        return img
    img = BytesIO(img)
    img.seek(0)
    return decompress_bitmap(img)


def decompress_path(path):
    return decompress_bitmap(open(path, 'rb'))


def compress(im):
    h, w = im.shape
    buf = 255*(im.flatten()> 126).astype(int)
    color = -1
    count = 0
    out = b''
    a = 0
    for c in buf[::-1]:
        if color < 0:
            color = c
        if color == c:
            count += 1
        if color != c or count == 255:
            out += struct.pack(inbit_fmt, count, color)
            if count==255:
                count = 0
            else:
                count, color = 1, c
                
            
    if count:
        out += struct.pack(inbit_fmt, count, color)
    
    imglen = len(out)
    outH = list(outHeader[:])
    outH[0], outH[1] = 73, 77  # ESS Cookie
    outH[FILESIZE] = imglen+ outH[OFFSET]
    outH[WIDTH] = w
    outH[HEIGHT] = h
    outH[COMPRESSION] = 9  # ESS Compression
    outH[IMAGESIZE] = imglen
    
    header = struct.pack(bitmapHeader_fmt, *tuple(outH)) 
    return header + colormap_bin + out
        
