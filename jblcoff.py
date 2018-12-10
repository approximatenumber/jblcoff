# JBL Cut Off - workaround of stupid JBL silence cutting off "feature".

import wx
import wx.media

AUDIOFILE = 'cuckoo.wav'

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(250,150))

        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetStatusText('Press Start.')
        
        self.start_button = wx.Button(self,
                                      label='Start')
        self.stop_button = wx.Button(self,
                                     label='Stop')
        self.stop_button.Disable()

        self.start_button.Bind(wx.EVT_BUTTON, self.OnStartButton)
        self.stop_button.Bind(wx.EVT_BUTTON, self.OnStopButton)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.start_button, 0, wx.CENTER)
        sizer.Add(self.stop_button, 0, wx.CENTER)
        self.SetSizer(sizer)
        self.Show(True)

    def OnStartButton(self, evt):
        self.play_sound()
        self.start_button.Disable()
        self.stop_button.Enable()
        self.status_bar.SetStatusText('Playing %s' % AUDIOFILE)

    def OnStopButton(self, evt):
        self.stop_sound()
        self.stop_button.Disable()
        self.start_button.Enable()
        self.status_bar.SetStatusText('Stopped.')

    def play_sound(self):
        try:
            self.mc = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER)
            self.mc.Load(AUDIOFILE)
            self.mc.Play()
        except:
            wx.MessageBox("Invalid sound file", "Error")

    def stop_sound(self):
        self.mc.Stop()

app = wx.App(False)
frame = MainWindow(None, "JBL Cut Off :-|")
app.MainLoop()
