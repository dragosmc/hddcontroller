__author__ = 'dragosmc'

import usb.core
import usb.util
import usb.control
import usb.backend
import base64
interface = 0


def get_devices():
    dev_list = usb.core.find(idVendor=0x152d, idProduct=0x2339)
    print dev_list
    return dev_list

dev = get_devices()
cfg = dev.get_active_configuration()
# cfg.set()
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None
dev.write(ep.bEndpointAddress,'\xEC')
collected = 0
attempts = 50
while collected < attempts:
    data =  dev.read(ep.bEndpointAddress,ep.wMaxPacketSize )
    print data
    collected+=1

# print ep.bEndpointAddress
# print ep.wMaxPacketSize

# print "Wrote to the first endpoint"
# print ep.read(512,0)

if dev.is_kernel_driver_active(0) is True:
            print "but we need to detach kernel driver"
            dev.detach_kernel_driver(interface)
            print "claiming device"
            usb.util.claim_interface(dev, interface)

#             dev.write(1,'\xEC')
#             print "WRITEEEEEE"

            # ep.write('\xEC')


           # print "release claimed interface"
           # usb.util.release_interface(dev, interface)
           # print "now attaching the kernel driver again"
           # dev.attach_kernel_driver(interface)
           # print "all done"


