import ctypes
import fcntl
import struct

__author__ = 'dragosmc'

import usb.core
import usb.util
import usb.control
import usb.backend
import binascii
from array import array
interface = 0

class AtaCmd(ctypes.Structure):
  """ATA Command Pass-Through
     http://www.t10.org/ftp/t10/document.04/04-262r8.pdf"""

  _fields_ = [
      ('opcode', ctypes.c_ubyte),
      ('protocol', ctypes.c_ubyte),
      ('flags', ctypes.c_ubyte),
      ('features', ctypes.c_ubyte),
      ('sector_count', ctypes.c_ubyte),
      ('lba_low', ctypes.c_ubyte),
      ('lba_mid', ctypes.c_ubyte),
      ('lba_high', ctypes.c_ubyte),
      ('device', ctypes.c_ubyte),
      ('command', ctypes.c_ubyte),
      ('reserved', ctypes.c_ubyte),
      ('control', ctypes.c_ubyte) ]


class SgioHdr(ctypes.Structure):
  """<scsi/sg.h> sg_io_hdr_t."""

  _fields_ = [
      ('interface_id', ctypes.c_int),
      ('dxfer_direction', ctypes.c_int),
      ('cmd_len', ctypes.c_ubyte),
      ('mx_sb_len', ctypes.c_ubyte),
      ('iovec_count', ctypes.c_ushort),
      ('dxfer_len', ctypes.c_uint),
      ('dxferp', ctypes.c_void_p),
      ('cmdp', ctypes.c_void_p),
      ('sbp', ctypes.c_void_p),
      ('timeout', ctypes.c_uint),
      ('flags', ctypes.c_uint),
      ('pack_id', ctypes.c_int),
      ('usr_ptr', ctypes.c_void_p),
      ('status', ctypes.c_ubyte),
      ('masked_status', ctypes.c_ubyte),
      ('msg_status', ctypes.c_ubyte),
      ('sb_len_wr', ctypes.c_ubyte),
      ('host_status', ctypes.c_ushort),
      ('driver_status', ctypes.c_ushort),
      ('resid', ctypes.c_int),
      ('duration', ctypes.c_uint),
      ('info', ctypes.c_uint)]

def get_devices():
    dev_list = usb.core.find(idVendor=0x152d, idProduct=0x2339)
    print dev_list
    return dev_list

dev = get_devices()
#dev.set_configuration()
# if dev.is_kernel_driver_active(0) is True:
#    print "but we need to detach kernel driver"
#    dev.detach_kernel_driver(interface)
#    print "claiming device"
#    usb.util.claim_interface(dev, interface)

cfg = dev.get_active_configuration()
# cfg.set()
#print cfg
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None

#print data
  

print ep.bEndpointAddress
# print ep
# print ep.wMaxPacketSize

# print "Wrote to the first endpoint"
# print ep.read(512,0)

def SwapString(str):
  """Swap 16 bit words within a string.

  String data from an ATA IDENTIFY appears byteswapped, even on little-endian
  achitectures. I don't know why. Other disk utilities I've looked at also
  byte-swap strings, and contain comments that this needs to be done on all
  platforms not just big-endian ones. So... yeah.
  """
  s = []
  for x in range(0, len(str) - 1, 2):
    s.append(str[x+1])
    s.append(str[x])
  return ''.join(s).strip()

# feature = bytearray([0xD0])
# count = bytearray([0x00])
# lba = bytearray([0x00])
# device = bytearray([0x00])
# lbal = bytearray([0x00])
# lbam= bytearray([0x4F])
# lbah=bytearray([0xC2])

feature = bytearray([0x00])
count = bytearray([0x00])
lba = bytearray([0x000])
device = bytearray([0x00])
lbal = bytearray([0x00])
lbam= bytearray([0x00])
lbah=bytearray([0x00])
command = bytearray([0xEC]) #IDENTIFY DEVICE '\xEC'
c = device + count + lba  +  command

ata_cmd = AtaCmd(opcode=0xa1,  # ATA PASS-THROUGH (12)
               protocol=4<<1,  # PIO Data-In
               # flags field
               # OFF_LINE = 0 (0 seconds offline)
               # CK_COND = 1 (copy sense data in response)
               # T_DIR = 1 (transfer from the ATA device)
               # BYT_BLOK = 1 (length is in blocks, not bytes)
               # T_LENGTH = 2 (transfer length in the SECTOR_COUNT field)
               flags=0x2e,
               features=0, sector_count=0,
               lba_low=0, lba_mid=0, lba_high=0,
               device=0,
               command=0xec,  # IDENTIFY
               reserved=0, control=0)
ASCII_S = 83
SG_DXFER_FROM_DEV = -3
sense = ctypes.c_buffer(64)
identify = ctypes.c_buffer(512)
sgio = SgioHdr(interface_id=ASCII_S, dxfer_direction=SG_DXFER_FROM_DEV,
             cmd_len=ctypes.sizeof(ata_cmd),
             mx_sb_len=ctypes.sizeof(sense), iovec_count=0,
             dxfer_len=ctypes.sizeof(identify),
             dxferp=ctypes.cast(identify, ctypes.c_void_p),
             cmdp=ctypes.addressof(ata_cmd),
             sbp=ctypes.cast(sense, ctypes.c_void_p), timeout=3000,
             flags=0, pack_id=0, usr_ptr=None, status=0, masked_status=0,
             msg_status=0, sb_len_wr=0, host_status=0, driver_status=0,
             resid=0, duration=0, info=0)
SG_IO = 0x2285  # <scsi/sg.h>

# c =  device +command
# c = command + device +feature
print binascii.hexlify(ata_cmd)
print ep.bEndpointAddress

# with open('/dev/sdb', 'r') as fd:
#     if fcntl.ioctl(fd, SG_IO, ctypes.addressof(sgio)) != 0:
#         print "failed"
#
#     serial_no = SwapString(identify[10:19])
#     fw_rev = SwapString(identify[27:46])
#     model = SwapString(identify[0:511])
#     print ctypes.sizeof(identify)
#     print serial_no
#     print fw_rev
#     print model

def GetDriveId(dev):
  """Return information from interrogating the drive.

  This routine issues a HDIO_GET_IDENTITY ioctl to a block device,
  which only root can do.

  Args:
    dev: name of the device, such as 'sda' or '/dev/sda'

  Returns:
    (serial_number, fw_version, model) as strings
  """
  # from /usr/include/linux/hdreg.h, struct hd_driveid
  # 10H = misc stuff, mostly deprecated
  # 20s = serial_no
  # 3H  = misc stuff
  # 8s  = fw_rev
  # 40s = model
  # ... plus a bunch more stuff we don't care about.
  struct_hd_driveid = '@ 10H 20s 3H 8s 40s'
  HDIO_GET_IDENTITY = 0x0030d
  if dev[0] != '/':
    dev = '/dev/' + dev
  fd = open('/dev/sdb', 'r')
  print fd
  if fd  != None:
    #if fcntl.ioctl(fd, SG_IO, ctypes.addressof(sgio)) != 0:
    if fcntl.ioctl(fd, HDIO_GET_IDENTITY, 512) != 0:
        print "failed"
    fields = struct.unpack_from(struct_hd_driveid, buf)
    serial_no = fields[10].strip()
    fw_rev = fields[14].strip()
    model = fields[15].strip()
    return (serial_no, fw_rev, model)

print GetDriveId('sdb')
#print(ep.write(command,0))
# print(ep.read(512))
print(dev.write(0x2,ata_cmd,0))
print(dev.read(0x81,512,1000))

# for bRequest in range(255):
#     try:
#         read = dev.ctrl_transfer(0x81, bRequest, 0, 0, 8) #read 8 bytes
#         print "bRequest ", bRequest
#         print read
#     except:
#         # failed to get data for this request
#         pass
#
# data =  dev.read(0x81,ep.wMaxPacketSize)
# print data

#             dev.write(1,'\xEC')
#             print "WRITEEEEEE"

            # ep.write('\xEC')


  #print "release claimed interface"
  #usb.util.release_interface(dev, interface)
  #print "now attaching the kernel driver again"
  #dev.attach_kernel_driver(interface)
  #print "all done"


