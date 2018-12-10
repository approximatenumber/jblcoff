#!/usr/bin/env python

"""
JBL Cut Off - workaround of stupid JBL silence cutting off "feature".
It simply loops 20Hz audio file to prevent cutting off audio
after a few seconds of silence.
"""

import wx
import wx.media
import os

AUDIOFILE = '20hz-tone.wav'


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(250, 200))

        self.mc = wx.media.MediaCtrl(self)
        self.mc.Bind(wx.media.EVT_MEDIA_FINISHED, self.LoopSound)

        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetStatusText('Press Start.')

        self.start_button = wx.Button(self,
                                      label='Start')
        self.stop_button = wx.Button(self,
                                     label='Stop')
        self.stop_button.Disable()

        self.set_volume_control()

        self.start_button.Bind(wx.EVT_BUTTON, self.OnStartButton)
        self.stop_button.Bind(wx.EVT_BUTTON, self.OnStopButton)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.start_button, 0, wx.CENTER)
        sizer.Add(self.stop_button, 0, wx.CENTER)
        sizer.Add(self.volume, 0, wx.CENTER)
        self.SetSizer(sizer)
        self.Show(True)
        self.Center()

    def OnStartButton(self, evt):
        try:
            self.play_sound()
            self.start_button.Disable()
            self.stop_button.Enable()
            self.status_bar.SetStatusText('Playing %s' % AUDIOFILE)
        except:
            wx.MessageBox("Invalid sound file: %s" % AUDIOFILE, "Error")

    def OnStopButton(self, evt):
        self.stop_sound()
        self.stop_button.Disable()
        self.start_button.Enable()
        self.status_bar.SetStatusText('Stopped.')

    def LoopSound(self, evt):
        self.play_sound()

    def play_sound(self):
        if not os.path.isfile(AUDIOFILE):
            raise
        self.mc.Load(AUDIOFILE)
        self.mc.Play()

    def stop_sound(self):
        self.mc.Stop()

    def set_volume_control(self):
        self.volume = wx.Slider(self,
                                style=wx.SL_VERTICAL | wx.SL_INVERSE,
                                size=(100, 100))
        self.volume.SetRange(0, 100)
        self.currentVolume = 50
        self.volume.SetValue(self.currentVolume)
        self.volume.Bind(wx.EVT_SLIDER, self.onSetVolume)

    def onSetVolume(self, event):
        """Set the volume of the music player."""
        self.currentVolume = self.volume.GetValue()
        self.mc.SetVolume(float(self.currentVolume) / 100)


app = wx.App(False)
frame = MainWindow(None, "JBL Cut Off :-|")
app.MainLoop()
