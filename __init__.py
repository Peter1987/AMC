'''
Created on May 21, 2012

@author: peter
'''

import wx, os, DataReader, HilbertVis
import threading
#from wx.lib.pubsub import Publisher
import time
from rpy2.robjects import r


def scale_bitmap(bitmap, width, height):
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    image = image.Mirror(False)
    result = wx.BitmapFromImage(image)
    return result

class MyFrame(wx.Frame):
    '''
  
    '''
    x = 500
    y = 500
    start = True
    def __init__(self, parent, Id, title):
        
        self._hasDragged = False
        wx.Frame.__init__(self, parent, Id, title, wx.DefaultPosition, wx.Size(1000, 750))
        self.settings = Columns(None, -1,self)
        
        self.pnl1 = wx.Panel(self, -1, style = wx.SIMPLE_BORDER | wx.TAB_TRAVERSAL)
        self.pnl4 = wx.Panel(self, -1, style = wx.SIMPLE_BORDER |  wx.TAB_TRAVERSAL)
        self.pnl2 = wx.Panel(self, -1, style = wx.SIMPLE_BORDER |  wx.TAB_TRAVERSAL)
        self.pnl5 = wx.Panel(self, -1, style = wx.SIMPLE_BORDER |  wx.TAB_TRAVERSAL)
        self.pnl3 = wx.Panel(self, -1, style = wx.SIMPLE_BORDER | wx.TAB_TRAVERSAL)
        

        
        self.SetPosition((150,200))
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox3 = wx.BoxSizer(wx.VERTICAL)
        vbox4 = wx.BoxSizer(wx.VERTICAL)
        
        self.timer = wx.Timer(self)

        menubar = wx.MenuBar()
        file = wx.Menu()
        help = wx.Menu()
        submenu = wx.Menu()
        submenu.Append(201, 'Save &HTML\tCtrl+H', 'Save information and image to a HTML format')
        submenu.Append(202, 'Save Plain &Text\tCtrl+T', 'Save information to a plain text format')
        file.Append(101, '&Open\tCtrl+O', 'Open a new document')
        file.AppendMenu(102, '&Save', submenu,'Save Menu' )
        file.AppendSeparator()
        self.infomenu = help.Append(301, "&Information\tCtrl+I", 'Show data informnation')
        help.Append(302, "&About\tCtrl+A", 'Show application information')
        quit = wx.MenuItem(file, 105, '&Quit\tCtrl+Q', 'Quit the Application')
        file.AppendItem(quit)
        menubar.Append(file, '&File')
        menubar.Append(help, '&Help')
        self.SetMenuBar(menubar)
        
        wx.StaticText(self.pnl1,-1,"File:", pos = (5,5))
        self.pnl1filenamectrl = wx.TextCtrl(self.pnl1,-1,"", pos = (5,30),size = (450,-1))
        self.pnl1loadinginfo = wx.StaticText(self.pnl1,-1,"",pos = (5,60))
        
        
        #wx.Button(self.pnl1, 2, "show selected coulmuns", pos = (350,2))  
        self.generate = wx.Button(self.pnl2,3,"Generate picture", pos = (5,40))
        self.picvalue = wx.ComboBox(self.pnl2, -1,choices = [],pos = (5,5),style = wx.CB_READONLY)
        self.btn = wx.Button(self.pnl2, 4,  "Zoom on", pos = (5,75))
        



        hbox1.Add(self.pnl1, 1, wx.EXPAND | wx.ALL, 1)
        vbox1.Add(hbox3, 1, wx.EXPAND | wx.ALL, 1)
        vbox1.Add(hbox4, 1, wx.EXPAND | wx.ALL, 1)
        
        hbox3.Add(self.pnl2, 1, wx.EXPAND | wx.ALL, 1)
        hbox4.Add(self.pnl3, 1, wx.EXPAND | wx.ALL, 1)
        vbox2.Add(self.pnl4, 1, wx.EXPAND | wx.ALL, 1)
        vbox3.Add(self.pnl5, 1, wx.EXPAND | wx.ALL, 1)
        
        hbox2.Add(vbox1, 2, wx.EXPAND | wx.ALL, 1)
        hbox2.Add(vbox2, 4, wx.EXPAND | wx.ALL, 1)
        hbox2.Add(vbox3, 1, wx.EXPAND | wx.ALL, 1)
        
        vbox4.Add(hbox1, 1, wx.EXPAND | wx.ALL, 1)
        vbox4.Add(hbox2, 5, wx.EXPAND | wx.ALL, 1)
        
        
        self.Bind(wx.EVT_MENU,self.OnQuit, id = 105)
        self.Bind(wx.EVT_MENU,self.OnOpen, id = 101)
        self.Bind(wx.EVT_TIMER, self.UpdateScreen, self.timer)
        self.Bind(wx.EVT_MENU, self.InfoDec, id = 301)
        self.Bind(wx.EVT_BUTTON,self.Columns, id = 1)
        self.Bind(wx.EVT_BUTTON,self.ShowColumns, id = 2)
        self.Bind(wx.EVT_BUTTON,self.Generate, id = 3)
        #self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.btn.Bind(wx.EVT_KEY_DOWN, self.zoom)
        
        
        
        self.infomenu.Enable(0)
        self.generate.Enable(0)
        self.btn.Enable(0)
        
        self.SetSizer(vbox4)
        vbox4.Fit(self)
        
        self.pnl1.SetBackgroundColour("light grey")
        self.pnl2.SetBackgroundColour("light grey")
        self.pnl3.SetBackgroundColour("light grey")
        self.pnl4.SetBackgroundColour("light grey")
        self.pnl5.SetBackgroundColour("light grey")
        self.CreateStatusBar()
        
        self.__infot = wx.StaticText(self.pnl5, -1, "",pos = (5,5))
        
        

        



# Getters and Setters

    def GetColumns(self):
        columns = ["CHROM","POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO"]
        return columns

    def GetDir(self):
        return self.__dir
    
    def GetFile(self):
        return self.__file
    
    def SetDir(self,dir):
        self.__dir = dir
        
    def SetFile(self,file):
        self.__file = file
    
    def GetPath(self):
        return os.path.join(self.__dir,self.__file)

    def GetLoadInfo(self):
        return self.__loadinfo
    
    def SetLoadInfo(self,loadinfo):
        self.__loadinfo = loadinfo
        
        
#Functions

    def zoom(self,e):
        if e.GetKeyCode() == 388 or e.GetKeyCode() == 61:
            self.x += 50
            self.y += 50
            #if self.x > self.largeimagesize[0] or self.y > self.largeimagesize[1]:
            #    self.x = self.largeimagesize[0]
            #    self.y = self.largeimagesize[1]
            self.largeimagesize
            bitmap = scale_bitmap(self.bmp, self.x, self.y)
            self.sbmp.SetBitmap(bitmap)
        
        elif e.GetKeyCode() == 390 or e.GetKeyCode() == 45:
            self.x -= 50
            self.y -= 50
            #if self.x < self.smallimagesize[0] or self.y < self.smallimagesize[1]:
            #    self.x = self.smallimagesize[0]
            #    self.y = self.smallimagesize[1]
            bitmap = scale_bitmap(self.bmp, self.x, self.y)
            self.sbmp.SetBitmap(bitmap)
            
        
        elif e.GetKeyCode() == 316:
            self.sbmp.SetPosition((self.sbmp.GetPosition()[0]-10,self.sbmp.GetPosition()[1]))
            if self.sbmp.GetPosition()[0]+self.sbmp.GetSize()[0]<self.pnl2.GetSize()[0]-1:
                self.sbmp.SetPosition((self.pnl2.GetSize()[0]-self.sbmp.GetSize()[0],self.sbmp.GetPosition()[1]))
            
        
        elif e.GetKeyCode() == 314:
            self.sbmp.SetPosition((self.sbmp.GetPosition()[0]+(10),self.sbmp.GetPosition()[1]))
            if self.sbmp.GetPosition()[0]>0:
                self.sbmp.SetPosition((0, self.sbmp.GetPosition()[1]))
            
            
        elif e.GetKeyCode() == 315:
            self.sbmp.SetPosition((self.sbmp.GetPosition()[0],self.sbmp.GetPosition()[1]+(10)))
            if self.sbmp.GetPosition()[1]> 0:
                self.sbmp.SetPosition((self.sbmp.GetPosition()[0],10))
            
        elif e.GetKeyCode() == 317:
            self.sbmp.SetPosition((self.sbmp.GetPosition()[0],self.sbmp.GetPosition()[1]-10))
            if self.sbmp.GetPosition()[1] + self.sbmp.GetSize()[1]<self.pnl2.GetSize()[1]-1:
                self.sbmp.SetPosition((self.sbmp.GetPosition()[0],self.pnl2.GetSize()[1]-self.sbmp.GetSize()[1]))
        
        self.CalCoor()
        '''
        
        if event.GetKeyCode() == 388 or event.GetKeyCode() == 61:
            self.dc.Clear()
            self.dc2.Clear()
            W = float(self.img2.GetWidth())
            H = float(self.img2.GetHeight())
            self.img2 = self.img2.Scale(W+5*W/self.img1.GetWidth(),H+5*H/self.img1.GetHeight())
            self.img4 = wx.BitmapFromImage(self.img2)
            self.scaletup += 0.02*1.66
            self.dc2.DrawBitmapPoint( self.img4, (0,0))
            self.dc.DrawBitmapPoint( self.img3, (0,0))
            self.dc.SetPen(wx.Pen(wx.RED, 1))
            self.topline = (self.topline[0], self.topline[1], self.topline[2]-5, self.topline[3])
            self.bottomline = (self.bottomline[0], self.bottomline[1]-5, self.bottomline[2]-5, self.bottomline[3]-5)
            self.leftline = (self.leftline[0], self.leftline[1], self.leftline[2], self.leftline[3]-5)
            self.rightline = (self.rightline[0]-5, self.rightline[1], self.rightline[2]-5, self.rightline[3]-5)
            self.dc.DrawLine(self.topline[0],self.topline[1],self.topline[2],self.topline[3])
            self.dc.DrawLine(self.bottomline[0],self.bottomline[1],self.bottomline[2],self.bottomline[3])
            self.dc.DrawLine(self.leftline[0],self.leftline[1],self.leftline[2],self.leftline[3])
            self.dc.DrawLine(self.rightline[0],self.rightline[1],self.rightline[2],self.rightline[3])
                
        elif event.GetKeyCode() == 390 or event.GetKeyCode() == 45:
            W = self.img2.GetWidth()
            H = self.img2.GetHeight()
            self.img2 = self.img2.Scale(W-10,H-10)
            self.img4 = wx.BitmapFromImage(self.img2)
            self.dc.Clear()
            self.dc2.Clear()
            self.dc2.DrawBitmapPoint( self.img4, (0,0))
            self.dc.DrawBitmapPoint( self.img3, (0,0))
            self.dc.SetPen(wx.Pen(wx.RED, 1))
            self.topline = (self.topline[0], self.topline[1], self.topline[2]+5, self.topline[3])
            self.bottomline = (self.bottomline[0], self.bottomline[1]+5, self.bottomline[2]+5, self.bottomline[3]+5)
            self.leftline = (self.leftline[0], self.leftline[1], self.leftline[2], self.leftline[3]+5)
            self.rightline = (self.rightline[0]+5, self.rightline[1], self.rightline[2]+5, self.rightline[3]+5)
            self.dc.DrawLine(self.topline[0],self.topline[1],self.topline[2],self.topline[3])
            self.dc.DrawLine(self.bottomline[0],self.bottomline[1],self.bottomline[2],self.bottomline[3])
            self.dc.DrawLine(self.leftline[0],self.leftline[1],self.leftline[2],self.leftline[3])
            self.dc.DrawLine(self.rightline[0],self.rightline[1],self.rightline[2],self.rightline[3])
        
        elif event.GetKeyCode() == 314 or event.GetKeyCode() == 315 or event.GetKeyCode() == 316 or event.GetKeyCode() == 317:
            if event.GetKeyCode() == 316:
                if self.topline[2]+4 < self.imageCtrl.GetPosition()[0]+self.imageCtrl.GetSize()[0]:
                    self.dc2.Clear()
                    self.dc2.SetUserScale(self.scaletup,self.scaletup)
                    self.picturepos[0]-=10
                    self.dc2.DrawBitmapPoint( self.img4, (self.picturepos[0],self.picturepos[1]))
                    self.dc.Clear()
                    self.dc.DrawBitmapPoint( self.img3, (0,0))
                    self.dc.SetPen(wx.Pen(wx.RED, 1))
                    self.topline = (self.topline[0]+5, self.topline[1], self.topline[2]+5, self.topline[3])
                    self.bottomline = (self.bottomline[0]+5, self.bottomline[1], self.bottomline[2]+5, self.bottomline[3])
                    self.leftline = (self.leftline[0]+5, self.leftline[1], self.leftline[2]+5, self.leftline[3])
                    self.rightline = (self.rightline[0]+5, self.rightline[1], self.rightline[2]+5, self.rightline[3])
                    self.dc.DrawLine(self.topline[0],self.topline[1],self.topline[2],self.topline[3])
                    self.dc.DrawLine(self.bottomline[0],self.bottomline[1],self.bottomline[2],self.bottomline[3])
                    self.dc.DrawLine(self.leftline[0],self.leftline[1],self.leftline[2],self.leftline[3])
                    self.dc.DrawLine(self.rightline[0],self.rightline[1],self.rightline[2],self.rightline[3])
                    
            elif event.GetKeyCode() == 314:
                if self.topline[0]-4 > self.imageCtrl.GetPosition()[0]:
                    self.dc.Clear()
                    self.dc2.Clear()
                    self.picturepos[0]+=10
                    self.dc2.DrawBitmapPoint( self.img4, (self.picturepos[0],self.picturepos[1]))
                    self.dc.DrawBitmapPoint( self.img3, (0,0))
                    self.dc.SetPen(wx.Pen(wx.RED, 1))
                    self.topline = (self.topline[0]-5, self.topline[1], self.topline[2]-5, self.topline[3])
                    self.bottomline = (self.bottomline[0]-5, self.bottomline[1], self.bottomline[2]-5, self.bottomline[3])
                    self.leftline = (self.leftline[0]-5, self.leftline[1], self.leftline[2]-5, self.leftline[3])
                    self.rightline = (self.rightline[0]-5, self.rightline[1], self.rightline[2]-5, self.rightline[3])
                    self.dc.DrawLine(self.topline[0],self.topline[1],self.topline[2],self.topline[3])
                    self.dc.DrawLine(self.bottomline[0],self.bottomline[1],self.bottomline[2],self.bottomline[3])
                    self.dc.DrawLine(self.leftline[0],self.leftline[1],self.leftline[2],self.leftline[3])
                    self.dc.DrawLine(self.rightline[0],self.rightline[1],self.rightline[2],self.rightline[3])
            elif event.GetKeyCode() == 315:
                if self.topline[1]> self.imageCtrl.GetPosition()[1]:
                    self.dc.Clear()
                    self.dc2.Clear()
                    self.picturepos[1]+=10
                    self.dc2.DrawBitmapPoint( self.img4, (self.picturepos[0],self.picturepos[1]))
                    self.dc.DrawBitmapMirrorPoint( self.img3, (0,0))
                    self.dc.SetPen(wx.Pen(wx.RED, 1))
                    self.topline = (self.topline[0], self.topline[1]-5, self.topline[2], self.topline[3]-5)
                    self.bottomline = (self.bottomline[0], self.bottomline[1]-5, self.bottomline[2], self.bottomline[3]-5)
                    self.leftline = (self.leftline[0], self.leftline[1]-5, self.leftline[2], self.leftline[3]-5)
                    self.rightline = (self.rightline[0], self.rightline[1]-5, self.rightline[2], self.rightline[3]-5)
                    self.dc.DrawLine(self.topline[0],self.topline[1],self.topline[2],self.topline[3])
                    self.dc.DrawLine(self.bottomline[0],self.bottomline[1],self.bottomline[2],self.bottomline[3])
                    self.dc.DrawLine(self.leftline[0],self.leftline[1],self.leftline[2],self.leftline[3])
                    self.dc.DrawLine(self.rightline[0],self.rightline[1],self.rightline[2],self.rightline[3])
            elif event.GetKeyCode() == 317:
                if self.bottomline[1] < self.imageCtrl.GetPosition()[1]+self.imageCtrl.GetSize()[1]:
                    self.dc2.Clear()
                    self.picturepos[1]-=10
                    self.dc2.DrawBitmapPoint( self.img4, (self.picturepos[0],self.picturepos[1]))
                    self.dc.Clear()
                    self.dc.DrawBitmapPoint( self.img3, (0,0))
                    self.dc.SetPen(wx.Pen(wx.RED, 1))
                    self.topline = (self.topline[0], self.topline[1]+5, self.topline[2], self.topline[3]+5)
                    self.bottomline = (self.bottomline[0], self.bottomline[1]+5, self.bottomline[2], self.bottomline[3]+5)
                    self.leftline = (self.leftline[0], self.leftline[1]+5, self.leftline[2], self.leftline[3]+5)
                    self.rightline = (self.rightline[0], self.rightline[1]+5, self.rightline[2], self.rightline[3]+5)
                    self.dc.DrawLine(self.topline[0],self.topline[1],self.topline[2],self.topline[3])
                    self.dc.DrawLine(self.bottomline[0],self.bottomline[1],self.bottomline[2],self.bottomline[3])
                    self.dc.DrawLine(self.leftline[0],self.leftline[1],self.leftline[2],self.leftline[3])
                    self.dc.DrawLine(self.rightline[0],self.rightline[1],self.rightline[2],self.rightline[3])
                    
        '''
    def CalCoor(self):
        size = 2**self.__hil.GetSize()
        self.__coorx = []
        pxl = float(self.pnl2.GetSize()[0])/(float(self.pnl2.GetSize()[0])/float(self.sbmp.GetSize()[0])*float(size))
        n = 0
        m = 0
        k = pxl
        for i in range(self.sbmp.GetSize()[0]):
            self.__coorx.append(n)
            m+=1
            if m> k:
                k += pxl
                n+=1
        self.__coory = []
        pxl = float(self.pnl2.GetSize()[1])/(float(self.pnl2.GetSize()[1])/float(self.sbmp.GetSize()[1])*float(size))
        n = 0
        m = 0
        k = pxl
        for i in range(self.sbmp.GetSize()[0]):
            self.__coory.append(n)
            m+=1
            if m> k:
                k += pxl
                n+=1
    '''
    def Zoom(self, event):
        h = self.img2.GetHeight()
        w = self.img2.GetWidth()
        newWidth = int(round(float(w) * self.scale))
        newHeight = int(round(float(h) * self.scale))
        
        self.img2.Rescale(newWidth, newHeight)
        #self.manageScrollbars(newWidth, newHeight, scale)
        #self.SetScrollbars(10, 10, newWidth/10, newHeight/10)
        self.display2()
    '''
    def Zoom(self,e):
        coor = int(self.coor.GetValue())
        self.x = coor
        self.y = coor
        bitmap = scale_bitmap(self.bmp, coor, coor)
        self.sbmp.SetBitmap(bitmap)
        self.CalCoor()
        
    def MMove(self,e):
        if self.start:
            self.CalCoor()
            self.start = False
        text = r('''
        hMat[{0},{1}]
        '''.format(self.__coorx[e.GetX()]+1,self.__coory[e.GetY()]+1))
        text = str(text).replace("[1]", ""+":  ")
        self.__infot.SetLabel(str(text))
        
    '''
    def display2(self):
        if self.img2:
            dc = wx.ClientDC(self)
            self.PrepareDC(dc)
            self.bitmap = self.img2.ConvertToBitmap()
            dc.DrawBitmap(self.bitmap, 0,0)
    '''


    def grabpicture(self,event):
        try:
            self.x = event.GetX()+self.difx
            self.y = event.GetY()+self.dify
        except:
            self.x = event.GetX()
            self.y = event.GetY()

    def info(self,event):
        #self.infotext.SetLabel("X = " + str(event.GetX()) + "\n" + "Y = " + str(event.GetY()))
        text = r('''
        hMat[{0},{1}]
        '''.format())
        self.__infot.SetLabel(str(text))
        #    try:
        #        self.__infot.SetLabel(str(event.GetX()+self.difx)+" - "+str(event.GetY()+self.dify))
        #    except:
        #        self.__infot.SetLabel(str(event.GetX())+" - "+str(event.GetY()))
        if event.LeftIsDown():
            if self._hasDragged:
                self.dc2.Clear()
                self.dc2.DrawBitmapPoint(self.img4, (self.picturepos[0]-self.difx,self.picturepos[1]-self.dify))
            else:
                self._hasDragged= True
            self.difx = self.x-event.GetX()
            self.dify = self.y-event.GetY()

    def InfoDec(self,event):
        description = [[],[]]
        for i in self.__vcf.GetInfoValues():
            description[0].append(i[0])
            description[1].append(i[3])
        self.__helptext = ""
        for i in range(len(description[0])):
            self.__helptext += str(description[0][i]) + " : " + str(description[1][i]) + "\n"
        dlg = wx.MessageDialog(self, self.__helptext, 'Info', wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def ShowColumns(self,event):
        try:
            for i in range(len(self.__infotext)):
                self.__infotext[i].Destroy()
        except:
            pass
        self.__infotext = []
        n = 5
        for i in self.settings.GetSelectedINFO():
            self.__infotext.append(wx.StaticText(self.pnl4,-1,i,pos = (5,n)))
            n += 30

    def Columns(self,event):
        self.settings.INFO(self.__vcf)
        self.settings.Show(1)

    def UpdateScreen(self,event):
        self.pnl1loadinginfo.SetLabel(self.GetLoadInfo())

    def OnQuit(self,event):
        dlg = wx.MessageBox( "Are you sure you want to quit", "Quit",wx.YES_NO | wx.CENTRE | wx.NO_DEFAULT)
        if dlg == wx.YES:
            self.Close()
            
    def OnOpen(self,event):
        wildcard = "VCF files (*.vcf)|*.vcf"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.SetLoadInfo("VCF file is loading. Please Wait.....")
            path = dialog.GetPath()
            self.SetDir(os.path.dirname(path))
            self.SetFile(os.path.basename(path))
            self.pnl1filenamectrl.SetValue(self.GetFile())
        dialog.Destroy()
        self.__vcf = DataReader.DataReader()
        try:
            self.__vcf.SetPath(self.GetPath())
            self.timer.Start(500)
            LoadVCF(self.__vcf,self)
            self.columnbutton = wx.Button(self.pnl1, 1, "Select columns", pos = (300,60))
            self.columnbutton.Enable(0)
        except AttributeError:
            pass
        
        
    def SetupPics(self):
        bmp = wx.Bitmap("temp/HGui.png", wx.BITMAP_TYPE_ANY)
        self.largeimagesize = [bmp.GetHeight(),bmp.GetWidth()]
        self.smallimagesize = [self.largeimagesize[0]/2,self.largeimagesize[1]/2]
        bitmap = scale_bitmap(bmp,self.smallimagesize[0],self.smallimagesize[1])
        self.sbmp = wx.StaticBitmap(self.pnl4, -1, bmp)
        self.sbmp.SetBitmap(bitmap)
        self.sbmp.Bind(wx.EVT_MOTION, self.MMove)
        self.sbmp.Bind(wx.EVT_LEFT_DOWN, self.InfoPrint)
        self.bmp = bmp
        
    def InfoPrint(self,event):
        text = r('''
        hMat[{0},{1}]
        '''.format(self.__coorx[event.GetX()]+1,self.__coory[event.GetY()]+1))
        dlg = wx.MessageDialog(self, str(text), 'Info', wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        
    '''
    def OnPaint(self,event):
        self.scaletup = 1
        self.picturepos = [0,0]
        self.dc = wx.PaintDC(self.pnl3)
        self.dc2 = wx.PaintDC(self.pnl4)
        self.dc.SetBackground( wx.Brush("light grey"))
        self.dc2.SetBackground(wx.Brush("light grey"))
        self.dc.Clear()
        self.dc2.Clear()
        try:
            self.img4 = wx.BitmapFromImage(self.img2)
            self.img3 = wx.BitmapFromImage(self.img1)
            self.dc.DrawBitmapPoint( self.img3, (0,0))
            self.dc2.DrawBitmapPoint( self.img4, (0,0))
        except:
            pass
        try:
            self.dc.SetPen(wx.Pen(wx.RED, 4))
            self.dc.DrawLine(self.topline[0],self.topline[1],self.topline[2],self.topline[3])
            self.dc.DrawLine(self.bottomline[0],self.bottomline[1],self.bottomline[2],self.bottomline[3])
            self.dc.DrawLine(self.leftline[0],self.leftline[1],self.leftline[2],self.leftline[3])
            self.dc.DrawLine(self.rightline[0],self.rightline[1],self.rightline[2],self.rightline[3])
            self.drawline = 0
        except:
            pass
        event.Skip()
        '''
        
        
        
    def Generate(self,event):
        sel = self.picvalue.GetValue()
        data = []
        for i in self.__vcf.GetINFO():
            data.append(i[sel])
        self.__hil = HilbertVis.Hilbert(data)
        #
        #img = wx.Image("temp/HGui.png")
        #self.imageCtrl = wx.StaticBitmap(self.pnl3, wx.ID_ANY,
        #                                 wx.BitmapFromImage(img),pos = (0,0),size = (self.pnl3.GetSize()[0],self.pnl3.GetSize()[1]))
        #img2 = wx.Image("temp/HGui.png")
        #self.imageCtrl2 = wx.StaticBitmap(self.pnl4, wx.ID_ANY,
        #                                 wx.BitmapFromImage(img2))
        #self.imageCtrl2.Bind(wx.EVT_MOTION,self.info)
        #self.imageCtrl2.Bind(wx.EVT_LEFT_DOWN,self.grabpicture)
        
        self.SetupPics()
        #self.Refresh()
        self.btn.Enable(1)
        


class LoadVCF(threading.Thread):
    def __init__(self,vcf,frame):
        threading.Thread.__init__(self)
        super(LoadVCF, self).__init__()
        self.__stop = threading.Event()
        self.__vcf = vcf
        self.__frame = frame
        self.start()
        
    def run(self):
        self.__vcf.Parser()
        self.__frame.SetLoadInfo("VCF file loading is done!")
        self.__frame.columnbutton.Enable(1)
        self.__frame.infomenu.Enable(1)
        self.__frame.generate.Enable(1)
        time.sleep(1)
        self.__frame.timer.Stop()



class Columns(wx.Dialog):
    def __init__(self, parent,ID, maingui):
        wx.Dialog.__init__(self, parent, ID, "Column Select",size = (950,500),style = wx.CAPTION|wx.CLOSE_BOX|wx.SYSTEM_MENU)
        self.__maingui = maingui
        
        self.__checks = []
        n=5
        id = 1
        for i in maingui.GetColumns():
            self.__checks.append(wx.CheckBox(self,id,i,pos = (5,n)))
            n += 25
            id += 1
        self.__id = id -1
        
        wx.Button(self, 100, "Ok", pos = (700,450))
        
        self.Bind(wx.EVT_CHECKBOX, self.INFOshow, id = self.__id)
        self.Bind(wx.EVT_BUTTON, self.CloseColumns, id = 100)
            
    
    def INFO(self,vcf):
        self.__vcf = vcf
        
    def INFOshow(self,event):
        try:
            for i in range(len(self.__info)):
                self.__info[i].Destroy()
        except:
            pass
        try:
            self.__infotext2.Destroy()
        except:
            pass
        self.__info = []
        description = [[],[]]
        for i in self.__vcf.GetInfoValues():
            description[0].append(i[0])
            description[1].append(i[3])
        n= 35
        m=0
        self.__infotext = wx.StaticText(self,-1,"INFO:", pos = (100,5))
        self.__infolist = []
        for i in self.__vcf.GetINFONames():
            self.__info.append(wx.CheckBox(self,-1,i+":     "+description[1][m],pos = (100,n)))
            self.__infolist.append(i)
            n += 25
            m+=1
        
        
    def GetSelectedINFO(self):
        infolist = []
        for i in self.__checks:
            if i.GetValue() == True:
                infolist.append(i.GetLabel())
        try:
            for i in self.__info:
                if i.GetValue() == True:
                    infolist.append(i.GetLabel().split(":")[0])
        except:
            pass
        return infolist
    
    def CHROM(self,vcf):
        pass
    
    def CloseColumns(self,event):
        description = [[],[]]
        for i in self.__vcf.GetInfoValues():
            description[0].append(i[0])
            description[1].append(i[2])
        list = []
        for i in range(len(self.GetSelectedINFO())):
            list.append(self.GetSelectedINFO()[i])
                
            '''
            for m in range(len(description)):
                description[m]
            if self.__vcf.GetInfoType()[n][0] == i:
                if self.__vcf.GetInfoType()[n][2] == "Integer" or self.__vcf.GetInfoType()[n][2] == "Float":
                    list.append(i)
            '''
        self.__maingui.picvalue.SetItems(list)
        self.Show(0)

        

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