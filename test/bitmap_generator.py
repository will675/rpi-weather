#!/usr/bin/env python
#===============================================================================
# bitmap_generator.py
# 
# 2016-08-10
# Created from code snippet held in header of led8x8icons.py
#===============================================================================

BITMAP = [
[0, 0, 0, 0, 0, 0, 0, 0,],
[0, 0, 0, 1, 0, 0, 0, 0,],
[1, 1, 0, 1, 0, 1, 0, 0,],
[0, 0, 1, 1, 1, 0, 0, 0,],
[0, 0, 1, 0, 1, 1, 1, 0,],
[0, 0, 0, 0, 1, 0, 0, 0,],
[1, 1, 1, 1, 0, 1, 0, 0,],
[0, 0, 0, 0, 0, 0, 0, 0,],
]
value = 0
for y,row in enumerate(BITMAP):
    row_byte = 0
    for x,bit in enumerate(row):
        row_byte += bit<<x    
    value += row_byte<<(8*y)
print '0x'+format(value,'02x')