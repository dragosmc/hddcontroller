import ctypes
import fcntl
import struct

__author__ = 'root'

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
  HDIO_GET_IDENTITY = 0x030d
  if dev[0] != '/':
    dev = '/dev/' + dev
  with open(dev, 'r+') as fd:
    buf = fcntl.ioctl(fd, HDIO_GET_IDENTITY, '' * 512)
    fields = struct.unpack_from(struct_hd_driveid, buf)
    serial_no = fields[10].strip()
    fw_rev = fields[14].strip()
    model = fields[15].strip()
    return (serial_no, fw_rev, model)

t = GetDriveId('/dev/sdb')
print (t)
