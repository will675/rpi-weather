#===============================================================================
# led8x8icons.py
#
# Dictionary of LED 8x8 matrix icons as 64 bit values.
#
# Code snippet for computing value from bitmap:
#
#           BITMAP = [
#           [1, 1, 1, 1, 1, 1, 1, 1,],
#           [1, 1, 0, 0, 0, 0, 0, 1,],
#           [1, 0, 1, 0, 0, 0, 0, 1,],
#           [1, 0, 0, 1, 0, 0, 0, 1,],
#           [1, 0, 0, 0, 1, 0, 0, 1,],
#           [1, 0, 0, 0, 0, 1, 0, 1,],
#           [1, 0, 0, 0, 0, 0, 1, 1,],
#           [1, 0, 0, 0, 0, 0, 0, 1,],
#           ]
#           value = 0
#           for y,row in enumerate(BITMAP):
#               row_byte = 0
#               for x,bit in enumerate(row):
#                   row_byte += bit<<x    
#               value += row_byte<<(8*y)
#           print '0x'+format(value,'02x')
#
# Code snippet for setting individual LEDs on the display.
#
#        def set_raw64(value):
#            led8x8matrix.clear()
#            for y in xrange(8):
#                row_byte = value>>(8*y)
#                for x in xrange(8):
#                    pixel_bit = row_byte>>x&1 
#                    led8x8matrix.set_pixel(x,y,pixel_bit) 
#            led8x8mmatrix.write_display() 
#
# 2014-10-20
# Carter Nelson
#==============================================================================
LED8x8ICONS = {
#---------------------------------------------------------
# default
#---------------------------------------------------------
''                                  : 0x0000000000000000 ,    
#---------------------------------------------------------
# misc
#---------------------------------------------------------
'ALL_ON'                            : 0xffffffffffffffff ,
'ALL_OFF'                           : 0x0000000000000000 ,
'UNKNOWN'                           : 0x00004438006c6c00 ,
'BOTTOM_ROW'                        : 0xff00000000000000 ,
'TOP_ROW'                           : 0x00000000000000ff , 
'LEFT_COL'                          : 0x0101010101010101 ,
'RIGHT_COL'                         : 0x8080808080808080 ,
'BOX'                               : 0xff818181818181ff ,
'XBOX'                              : 0xffc3a59999a5c3ff ,
'MINUS'                             :       0x7c00000000 ,
'PLUS'                              :   0x10107c10100000 ,
#---------------------------------------------------------
# weather
#---------------------------------------------------------
'SUNNY'                             : 0x9142183dbc184289 ,
'RAIN'                              : 0x55aa55aa55aa55aa ,
'CLOUD'                             : 0x00007e818999710e ,
'SHOWERS'                           : 0x152a7e818191710e ,
'SNOW'                              : 0xa542a51818a542a5 ,
'STORM'                             : 0x0a04087e8191710e ,
'MOON'                              :  0xc18307030180c00 ,
'PART_CLOUD'                        :    0xf10347c7b3000 ,
'FOG'                               : 0x281038d610383810 ,
'HAIL'                              : 0x3892c7923892c792 ,

#---------------------------------------------------------
# digits
#---------------------------------------------------------
'-9'                                : 0x609080e790906000 ,
'-8'                                : 0x6090906790906000 ,
'-7'                                : 0x202020274080f000 ,
'-6'                                : 0x6090907710906000 ,
'-5'                                : 0x60908087f010f000 ,
'-4'                                : 0x404040f750604000 ,
'-3'                                : 0x6090806780906000 ,
'-2'                                : 0xf010204780906000 ,
'-1'                                : 0x7020202720302000 ,
'0'                                 : 0x38444c5464443800 ,
'1'                                 : 0x3810101014181000 ,
'2'                                 : 0x7c08102040443800 ,
'3'                                 : 0x3844403040443800 ,
'4'                                 : 0x20207c2428302000 ,
'5'                                 : 0x384440403c047c00 ,
'6'                                 : 0x3844443c04443800 ,
'7'                                 :  0x808081020407c00 ,
'8'                                 : 0x3844443844443800 , 
'9'                                 : 0x3844407844443800 ,
'10'                                : 0x6792929292936200 ,
'11'                                : 0x7722222222332200 ,
'12'                                : 0xf712224282936200 ,
'13'                                : 0x6792826282936200 ,
'14'                                : 0x474242f252634200 ,
'15'                                : 0x679282827213f200 ,
'16'                                : 0x6792927212936200 ,
'17'                                : 0x272222224283f200 ,
'18'                                : 0x6792926292936200 ,
'19'                                : 0x679282e292936200 ,
'20'                                : 0x6f91929498996600 ,
'21'                                : 0xef41424448694600 ,
'22'                                : 0xff11224488996600 ,
'23'                                : 0x6f91826488996600 ,
'24'                                : 0x4f4142f458694600 ,
'25'                                : 0x6f9182847819f600 ,
'26'                                : 0x6f91927418996600 ,
'27'                                : 0x2f2122244889f600 ,
'28'                                : 0x6f91926498996600 ,
'29'                                : 0x6f9182e498996600 ,
'30'                                : 0x6699989698996600 ,
'31'                                : 0xe649484648694600 ,
'32'                                : 0xf619284688996600 ,
'33'                                : 0x6699886688996600 ,
'34'                                : 0x464948f658694600 ,
'35'                                : 0x669988867819f600 ,
'36'                                : 0x6699987618996600 ,
'37'                                : 0x262928264889f600 ,
'38'                                : 0x6699986698996600 ,
'39'                                : 0x669988e698996600 ,

#---------------------------------------------------------
# kanji digits
#---------------------------------------------------------
'KANJI_0'                           : 0x3c4281818181423c ,
'KANJI_1'                           : 0x000000ff00000000 ,
'KANJI_2'                           : 0x00ff0000007e0000 ,
'KANJI_3'                           : 0xff00003c00007e00 ,
'KANJI_4'                           : 0x81ff81b3d59595ff ,
'KANJI_5'                           : 0xff44487e08087e00 ,
'KANJI_6'                           : 0x81422400ff080804 ,
'KANJI_7'                           : 0x788808087e080800 ,
'KANJI_8'                           : 0xc162241414141400 ,
'KANJI_9'                           : 0x61a22424243f0404 ,
}