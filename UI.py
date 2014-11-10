__author__ = 'dragosmc'

import wx
import hdd
import wx.lib.inspection

title = "HDD Controller"
list_button_label = "List devices"
clear_button_label = "Clear"


class StartUpPanel(wx.Panel):
    def __init__(self, *args, **kwargs):

        super(StartUpPanel, self).__init__(*args, **kwargs)

        panel = wx.Panel(self, size=(320, 120))
        panel.SetBackgroundColour(wx.RED)
        anotherpanel = wx.Panel(self, size=(320, 100))
        anotherpanel.SetBackgroundColour(wx.BLUE)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel)
        sizer.Add(anotherpanel)
        self.SetSizer(sizer)
        # start_button = wx.Button(panel, label="Start")
        # stop_button = wx.Button(panel, label="Stop")

         # self.next_panel_button = wx.Button(self, label="->")
        # self.temperature_text = wx.StaticText(self, label="Temperature")


        # text_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # text_sizer.Add(self.temperature_text, border=5)
        #
        # button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # button_sizer.Add(self.start_button, border=5)
        # button_sizer.Add(self.stop_button, border=5)
        #
        # next_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # next_sizer.Add(self.next_panel_button, border=5)
        #
        # main_sizer = wx.BoxSizer(wx.VERTICAL)
        # main_sizer.AddF(text_sizer,  wx.SizerFlags(1).Bottom().Right())
        # main_sizer.AddF(button_sizer, wx.SizerFlags(10).Bottom().Center().Expand())
        # main_sizer.AddF(next_sizer, wx.SizerFlags(1).Bottom().Right())
        # self.SetSizer(main_sizer)
        # self.SetAutoLayout(True)
        # main_sizer.Fit(self)


def button_pressed(event):
    devices = hdd.get_devices()
    for device in devices:
        deviceList.WriteText(str(device) + "\n\n\n")


def clear_pressed(event):
    deviceList.Clear()


app = wx.App()
frame = wx.Frame(None, size=(320,240), title=title)
#frame.SetClientSize((320,240))
mp = StartUpPanel(frame, size=(320,240))
# panel = wx.Panel(window)
#
# mainBox = wx.BoxSizer(wx.VERTICAL)
# topBox = wx.BoxSizer()
#
# listDevicesButton = wx.Button(panel, label=list_button_label)
# listDevicesButton.Bind(wx.EVT_BUTTON, button_pressed)
#
# deleteDevicesButton = wx.Button(panel, label=clear_button_label)
# deleteDevicesButton.Bind(wx.EVT_BUTTON, clear_pressed)
#
# deviceList = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.VSCROLL)
# deviceList.SetEditable(False)
#
# topBox.Add(listDevicesButton, flag=wx.LEFT, border=5)
# topBox.Add(deleteDevicesButton, flag=wx.RIGHT, border=5)
#
# mainBox.Add(topBox, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
# mainBox.Add(deviceList, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
#
# panel.SetSizer(mainBox)

wx.lib.inspection.InspectionTool().Show()
frame.Show()
frame.ShowFullScreen(True)
wx.CallLater(10000, frame.ShowFullScreen, False)
app.MainLoop()