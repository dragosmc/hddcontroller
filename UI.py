__author__ = 'dragosmc'

import wx
import hdd

title = "HDD Controller"
list_button_label = "List devices"
clear_button_label = "Clear"

def button_pressed(event):
    devices = hdd.get_devices()
    for device in devices:
        deviceList.WriteText(str(device) + "\n\n\n")

def clear_pressed(event):
    deviceList.Clear()

app = wx.App()
window = wx.Frame(None, title="HDD Controller", size=(800, 600), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
panel = wx.Panel(window)

mainBox = wx.BoxSizer(wx.VERTICAL)
topBox = wx.BoxSizer()

listDevicesButton = wx.Button(panel, label=list_button_label)
listDevicesButton.Bind(wx.EVT_BUTTON, button_pressed)

deleteDevicesButton = wx.Button(panel, label=clear_button_label)
deleteDevicesButton.Bind(wx.EVT_BUTTON, clear_pressed)

deviceList = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.VSCROLL)
deviceList.SetEditable(False)

topBox.Add(listDevicesButton, flag=wx.LEFT, border=5)
topBox.Add(deleteDevicesButton, flag=wx.RIGHT, border=5)

mainBox.Add(topBox, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
mainBox.Add(deviceList, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

panel.SetSizer(mainBox)
window.Show()
app.MainLoop()