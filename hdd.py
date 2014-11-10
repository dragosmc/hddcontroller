__author__ = 'dragosmc'

import usb.core
import usb.util
import usb.control
import usb.backend



def get_devices():
    dev_list = usb.core.find(find_all=True)
    return dev_list
