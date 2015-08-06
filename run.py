import os
import sys
import shutil
import wx
from wx.lib.wordwrap import wordwrap
import urllib2
import zipfile
import _winreg


class Frame(wx.Frame):
    def __init__(self, parent, title):
        super(Frame, self).__init__(parent, title=title, size=[400, 123],
                                    style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        self.wxpanel = wx.Panel(self)

        self.menuBar = wx.MenuBar()
        self.fileMenu = wx.Menu()
        self.aboutMenuItem = self.fileMenu.Append(wx.NewId(), "About",
                                                  "About the application")
        self.menuBar.Append(self.fileMenu, "&Info")
        self.SetMenuBar(self.menuBar)
        self.Bind(wx.EVT_MENU, self.about, self.aboutMenuItem)

        self.text = wx.StaticText(self.wxpanel, label="Point to CS:GO directory (Directory of csgo.exe)", pos=(2, 5.5))

        self.installpath = wx.TextCtrl(self.wxpanel, pos=(1, 26), size=[392, 23], style=wx.TE_READONLY)

        self.browsebut = wx.Button(self.wxpanel, label="Browse", pos=[306, 0])
        self.browsebut.Bind(wx.EVT_BUTTON, self.onbrowse)

        self.installbut = wx.Button(self.wxpanel, label="Install/Uninstall", pos=(0, 49), size=[394, 25])
        self.installbut.Bind(wx.EVT_BUTTON, self.onpress)
        self.installbut.Disable()

        self.cspath = None
        self.csgopath = None
        self.scriptspath = None
        self.slothmod = None

        self.Centre()
        self.Show()

    def about(self, event):
        licensetext = "Copyright 2015 10se1ucgo\r\n\r\nLicensed under the Apache License, Version 2.0" \
                      " (the \"License\");\r\nyou may not use this file except in compliance with the License" \
                      ".\r\nYou may obtain a copy of the License at\r\n\r\n" \
                      "    http://www.apache.org/licenses/LICENSE-2.0\r\n\r\nUnless required by applicable law or" \
                      " agreed to in writing, software\r\ndistributed under the License is distributed on an" \
                      " \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied." \
                      "\r\nSee the License for the specific language governing permissions and\r\nlimitations under " \
                      "the License."

        aboutpg = wx.AboutDialogInfo()
        aboutpg.Name = "About the SlothSquadron Mod Installer"
        aboutpg.Version = "v1.0"
        aboutpg.Copyright = "(c) 2015 10se1ucgo"
        aboutpg.Description = "A tool to install and uninstall SlothSquadron's weapon balance mod "
        aboutpg.WebSite = ("https://github.com/10se1ucgo/WeaponBalanceInstaller", "GitHub Project Page")
        aboutpg.License = wordwrap(licensetext, 500, wx.ClientDC(self))
        wx.AboutBox(aboutpg)

    def onbrowse(self, event):
        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST,
                           defaultPath=self.getcspath())

        if dlg.ShowModal() == wx.ID_OK:
            self.cspath = dlg.GetPath()
            self.checkdir()

        dlg.Destroy()

    def checkdir(self):
        try:
            if '730' in open(os.path.join(self.cspath, 'steam_appid.txt')).read():
                self.csgopath = os.path.join(self.cspath, "csgo")
                self.scriptspath = os.path.join(self.csgopath, "scripts")
                self.installpath.SetValue(self.cspath)

                print self.csgopath
                print self.scriptspath
                print self.cspath
                print os.getcwd()

                if os.path.isfile(os.path.join(self.scriptspath, "slothmod")):
                    self.slothmod = True
                    self.installbut.Enable()
                    self.installbut.SetLabel("Uninstall")
                    print "SLOTHMOD"
                else:
                    self.slothmod = False
                    self.installbut.Enable()
                    self.installbut.SetLabel("Install")
            else:
                self.wrongdir()

        except IOError:
            self.wrongdir()

    def onpress(self, event):
        if self.slothmod:
            print "Uninstalling sloth"
            shutil.rmtree(self.scriptspath)
            os.rename(self.scriptspath+"-original", self.scriptspath)
            sys.exit()
        else:
            self.downloadmod()
            os.rename(self.scriptspath, self.scriptspath+"-original")
            with zipfile.ZipFile("slothmod.zip", "r") as z:
                z.extractall(self.csgopath)
            open(os.path.join(self.scriptspath, "slothmod"), 'w').close()
            sys.exit()

    def wrongdir(self):
        warn = wx.MessageDialog(parent=self.wxpanel, message="This is not the CS:GO directory",
                                caption="ERROR", style=wx.OK | wx.ICON_WARNING)
        warn.ShowModal()
        warn.Destroy()
        self.onbrowse(wx.EVT_BUTTON)

    def getcspath(self):
        try:
            steam_reg_path = r"Software\Valve\Steam"
            reg_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, steam_reg_path, 0, _winreg.KEY_READ)
            value, regtype = _winreg.QueryValueEx(reg_key, r"SteamPath")
            return value + r"/steamapps/common/Counter-Strike Global Offensive"
        except WindowsError:
            return ""

    def downloadmod(self):
        dlurl = "https://www.dropbox.com/s/4b5kyp41c72k3la/slothmod.zip?dl=1"
        dl = urllib2.urlopen(dlurl)
        data = dl.read()
        dl.close()

        with open("slothmod.zip", "wb") as f:
            f.write(data)


if __name__ == '__main__':
    wxwindow = wx.App(False)
    Frame(None, title='SlothSquadron Mod Installer')  # Create Window
    wxwindow.MainLoop()
