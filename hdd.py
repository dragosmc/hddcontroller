import sys

import usb.core
import usb.util
import usb.control
import usb.backend

import wx

devList = usb.core.find(find_all=True)
if devList is None:
    print ("Moloz")
i = 0
print devList
for dev in devList:
    print dev
    print i
    i+=1
    sys.stdout.write(str(dev.bLength))

def buttonPressed(event):
    print "Button pressed"

app = wx.App()
window = wx.Frame(None)

button = wx.Button(window, label="Press me")
button.Bind(wx.EVT_BUTTON, buttonPressed)

window.Show()
app.MainLoop()


