#!/usr/bin/env python

"""
JBL Cut Off - workaround of stupid JBL silence cutting off "feature".
It simply loops 20Hz audio file to prevent cutting off audio
after a few seconds of silence.
"""

import wx
import wx.media
import os
import sys

AUDIOFILE = '20hz-tone.wav'


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        """Contructor."""
        wx.Frame.__init__(self, parent, title=title)
        self.panel = wx.Panel(self)
        self.panel.SetSize((250, 200))
        self.set_icon()

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
        sizer.Add(self.panel, 0, wx.CENTER)
        sizer.Add(self.start_button, 0, wx.CENTER)
        sizer.Add(self.stop_button, 0, wx.CENTER)
        sizer.Add(self.volume, 0, wx.CENTER)
        self.SetSizer(sizer)
        sizer.Layout()
        self.Layout()
        self.Show(True)
        self.Center()

    def OnStartButton(self, evt):
        """Actions for Start button."""
        try:
            wx.CallAfter(self.play_sound)
            self.start_button.Disable()
            self.stop_button.Enable()
            self.status_bar.SetStatusText('Playing %s' % AUDIOFILE)
        except:
            wx.MessageBox("Invalid sound file: %s" % AUDIOFILE, "Error")

    def OnStopButton(self, evt):
        """Actions for Stop button."""
        wx.CallAfter(self.stop_sound)
        self.stop_button.Disable()
        self.start_button.Enable()
        self.status_bar.SetStatusText('Stopped.')

    def LoopSound(self, evt):
        """Loop sound."""
        self.play_sound()

    def play_sound(self):
        """Play sound from file."""
        if not os.path.isfile(resource_path(AUDIOFILE)):
            raise
        self.mc.Load(resource_path(AUDIOFILE))
        self.mc.Play()

    def stop_sound(self):
        """Stop playing sound."""
        self.mc.Stop()

    def set_volume_control(self):
        """Add volume control."""
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

    def set_icon(self):
        """Set icon for app."""
        app_icon = wx.Icon(resource_path('app.ico'))
        self.SetIcon(app_icon)


def resource_path(relative_path):
    """Find static files inside pyinstaller bundle."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

app = wx.App(False)
frame = MainWindow(None, "JBL Cut Off :-|")
app.MainLoop()
