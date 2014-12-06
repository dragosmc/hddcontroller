__author__ = 'dragosmc'

import usb.core
import usb.util
import usb.control
import usb.backend
import binascii
from array import array
interface = 0


def get_devices():
    dev_list = usb.core.find(idVendor=0x152d, idProduct=0x2339)
    #print dev_list
    return dev_list

dev = get_devices()
#dev.set_configuration()
if dev.is_kernel_driver_active(0) is True:
    print "but we need to detach kernel driver"
    dev.detach_kernel_driver(interface)
    print "claiming device"
    usb.util.claim_interface(dev, interface)

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
# print ep.wMaxPacketSize

# print "Wrote to the first endpoint"
# print ep.read(512,0)



# feature = bytearray([0xD0])
# count = bytearray([0x00])
# lba = bytearray([0x00])
# device = bytearray([0x00])
# lbal = bytearray([0x00])
# lbam= bytearray([0x4F])
# lbah=bytearray([0xC2])

feature = bytearray([0x00])
count = bytearray([0x00])
lba = bytearray([0x00])
device = bytearray([0x10])
lbal = bytearray([0x00])
lbam= bytearray([0x00])
lbah=bytearray([0x00])
command = bytearray([0xE6]) #IDENTIFY DEVICE '\xEC'
c = device +command
# c =  device +command
# c = command + device +feature
print binascii.hexlify(c)
print ep.bEndpointAddress
#print(ep.write(command,0))
# print(ep.read(512))
print(dev.write(0x2,c,0))
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


