__author__ = 'dragosmc'

# typedef struct tagFIS_REG_H2D
# {
# 	// DWORD 0
# 	BYTE	fis_type;	// FIS_TYPE_REG_H2D
#
# 	BYTE	pmport:4;	// Port multiplier
# 	BYTE	rsv0:3;		// Reserved
# 	BYTE	c:1;		// 1: Command, 0: Control
#
# 	BYTE	command;	// Command register
# 	BYTE	featurel;	// Feature register, 7:0
#
# 	// DWORD 1
# 	BYTE	lba0;		// LBA low register, 7:0
# 	BYTE	lba1;		// LBA mid register, 15:8
# 	BYTE	lba2;		// LBA high register, 23:16
# 	BYTE	device;		// Device register
#
# 	// DWORD 2
# 	BYTE	lba3;		// LBA register, 31:24
# 	BYTE	lba4;		// LBA register, 39:32
# 	BYTE	lba5;		// LBA register, 47:40
# 	BYTE	featureh;	// Feature register, 15:8
#
# 	// DWORD 3
# 	BYTE	countl;		// Count register, 7:0
# 	BYTE	counth;		// Count register, 15:8
# 	BYTE	icc;		// Isochronous command completion
# 	BYTE	control;	// Control register
#
# 	// DWORD 4
# 	BYTE	rsv1[4];	// Reserved
# } FIS_REG_H2D;

class regH2d:
    def __init__(self):
        # DWORD 0
        self.fis_type = 0x34

        self.pmport = 0x0
        self.c = 0x01

        self.command = 0xEC
        self.feature = 0x00

        # DWORD 1
        self.lba0 = 0x00
        self.lba1 = 0x00
        self.lba2 = 0x00
        self.device = 0x0

        # DWORD 2
        self.lba3 = 0x00
        self.lba4 = 0x00
        self.lba5 = 0x00
        self.feature = 0x00

        # DWORD 3
        self.countl = 0x00
        self.counth = 0x00
        self.icc = 0x00
        self.control = 0x00

        # DWORD 4
        self.rsv1 = 0x0


    def to_byte_array(self):
        btrl = bytearray(self.fis_type)
        print binascii.hexlify(btrl)

        temp = bytearray(self.pmport)
        btrl = btrl + temp

        temp = bytearray(self.c)
        btrl = btrl + temp

        temp = bytearray(self.command)
        btrl = btrl + temp

        temp = bytearray(self.feature)
        btrl = btrl + temp

        temp = bytearray(self.lba0)
        btrl = btrl + temp

        temp = bytearray(self.lba1)
        btrl = btrl + temp

        temp = bytearray(self.lba2)
        btrl = btrl + temp

        temp = bytearray(self.device)
        btrl = btrl + temp

        temp = bytearray(self.lba3)
        btrl = btrl + temp

        temp = bytearray(self.lba4)
        btrl = btrl + temp

        temp = bytearray(self.lba5)
        btrl = btrl + temp

        temp = bytearray(self.feature)
        btrl = btrl + temp

        temp = bytearray(self.countl)
        btrl = btrl + temp

        temp = bytearray(self.counth)
        btrl = btrl + temp

        temp = bytearray(self.icc)
        btrl = btrl + temp

        temp = bytearray(self.control)
        btrl = btrl + temp

        return btrl




