'''
Created on May 21, 2012

@author: peter
'''

import wx



class MyFrame(wx.Frame):
    '''
  
    '''
    def __init__(self, parent, Id, title):
        wx.Frame.__init__(self, parent, Id, title, wx.DefaultPosition, wx.Size(500, 650))
        
        self.pnl1 = wx.Panel(self, -1, style = wx.SIMPLE_BORDER | wx.TAB_TRAVERSAL)
        self.pnl2 = wx.Panel(self, -1, style = wx.SIMPLE_BORDER |  wx.TAB_TRAVERSAL)
        self.SetPosition((500,200))
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        vbox1 = wx.BoxSizer(wx.VERTICAL)

        menubar = wx.MenuBar()
        file = wx.Menu()
        help = wx.Menu()
        submenu = wx.Menu()
        submenu.Append(201, 'Save HTML')
        submenu.Append(202, 'Save Plain Text')
        file.Append(101, '&Open', 'Open a new document')
        file.AppendMenu(102, '&Save', submenu)
        file.AppendSeparator()
        help.Append(301, "&Information", 'Show data informnation')
        help.Append(302, "&About", 'Show application information')
        quit = wx.MenuItem(file, 105, '&Quit\tCtrl+Q', 'Quit the Application')
        file.AppendItem(quit)
        menubar.Append(file, '&File')
        menubar.Append(help, '&Help')
        self.SetMenuBar(menubar)


        hbox1.Add(self.pnl1, 1, wx.EXPAND | wx.ALL, 1)
        hbox2.Add(self.pnl2, 1, wx.EXPAND | wx.ALL, 1)
        
        vbox1.Add(hbox1, 1, wx.EXPAND | wx.ALL, 1)
        vbox1.Add(hbox2, 5, wx.EXPAND | wx.ALL, 1)
        
        self.SetSizer(vbox1)

class MyApp(wx.App):
    '''
    Creates the frame
    :var frame: :class:`MyFrame()`
    '''
    def OnInit(self):
        frame = MyFrame(None, -1, "AMC Programm (Peter Admiraal)")
        frame.Show(True)
        return True

app = MyApp(0)
app.MainLoop()