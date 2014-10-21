__author__ = 'dragosmc'

import wx
import hdd


def button_pressed(event):
    devices = hdd.get_devices()
    for device in devices:
        deviceList.WriteText(str(device) + "\n\n\n")

app = wx.App()
window = wx.Frame(None, title="HDD Controller", size=(800, 600))
panel = wx.Panel(window)

mainBox = wx.BoxSizer(wx.VERTICAL)
topBox = wx.BoxSizer()

listDevicesButton = wx.Button(panel, label="List devices")
listDevicesButton.Bind(wx.EVT_BUTTON, button_pressed)

deviceList = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.VSCROLL)
deviceList.SetEditable(False)

topBox.Add(listDevicesButton, proportion=0.2, flag=wx.LEFT, border=5)

mainBox.Add(topBox, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
mainBox.Add(deviceList, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.LEFT | wx.LEFT, border=5)

panel.SetSizer(mainBox)
window.Show()
app.MainLoop()