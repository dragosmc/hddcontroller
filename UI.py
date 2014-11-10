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

        # Temp panel
        # - contains the "Temperature" text and placeholder for value
        temperature_panel = wx.Panel(self, size=(320, 50))
        temperature_panel.SetBackgroundColour(wx.RED)

        text = wx.StaticText(temperature_panel, name="temp_label", label="Temperature:")
        font =  wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL)
        text.SetFont(font)
        text.SetForegroundColour((0,0,0))

        self.temp = wx.TextCtrl(temperature_panel, name="temp_value_label", style=wx.TE_READONLY | wx.BORDER_NONE)
        self.temp.SetValue("14")
        self.temp.SetEditable(False)
        self.temp.SetForegroundColour((255,255,0))
        self.temp.SetBackgroundColour(wx.RED)

        temp_font =  wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL)
        self.temp.SetFont(temp_font)

        temperature_szr = wx.BoxSizer(wx.HORIZONTAL)
        temperature_szr.AddF(text, wx.SizerFlags().Centre())
        temperature_szr.AddF(self.temp, wx.SizerFlags().Centre())
        temperature_panel.SetSizer(temperature_szr)


        # Buttons panel
        # - contains the buttons and the sizer which layouts them
        buttons_panel = wx.Panel(self, size=(320, 140))
        buttons_panel.SetBackgroundColour(wx.BLUE)
        start_button = wx.Button(buttons_panel, name="btn_start", label="Start")
        stop_button = wx.Button(buttons_panel, name="btn_stop", label="Stop")
        buttons_panel_szr = wx.BoxSizer(wx.VERTICAL)
        buttons_panel_szr.AddMany({stop_button, start_button})
        buttons_panel.SetSizer(buttons_panel_szr)

        # Switch pane button's (control) panel
        control_panel = wx.Panel(self, size=(320, 50))
        control_panel.SetBackgroundColour(wx.GREEN)
        next_panel_button = wx.Button(control_panel, name="btn_next_panel", label="...")

        # Main sizer
        # - layout as per logbook
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddF(temperature_panel, wx.SizerFlags(1).Expand())
        sizer.AddF(buttons_panel, wx.SizerFlags(3).Expand())
        sizer.AddF(control_panel, wx.SizerFlags(1).Expand())
        self.SetSizer(sizer)

def button_pressed(event):
    devices = hdd.get_devices()
    for device in devices:
        deviceList.WriteText(str(device) + "\n\n\n")


def clear_pressed(event):
    deviceList.Clear()


app = wx.App()
frame = wx.Frame(None,title=title)
#frame.SetClientSize((320,240))
mp = StartUpPanel(frame)
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

#wx.lib.inspection.InspectionTool().Show()
frame.SetClientSize((320, 240))
frame.Show()

frame.ShowFullScreen(True)
#wx.CallLater(10000, frame.ShowFullScreen, False)
app.MainLoop()