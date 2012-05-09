import wx, os, sys, processes
from rpy2.robjects import r

class MyFrame(wx.Frame):
    '''
    Class makes a GUI with all the options avalable in the program
    
    :param parent: parent dialog.
    :type parent: int.
    :param id: Gui id.
    :type id: int.
    :param title: Gui title.
    :type title: string.
    :var self.CloseGraph: wx.Button
    :var self.pic: wx.Button
    :var self.x1: int
    :var self.x2: int
    :var self.y1: int
    :var self.y2: int
    
    
    '''
    def __init__(self, parent, Id, title):
        wx.Frame.__init__(self, parent, Id, title, wx.DefaultPosition, wx.Size(1324, 663))

        self.PhotoMaxSizeSmall = 325
        self.PhotoMaxSizeBig = self.PhotoMaxSizeSmall*2.01
        self.drawline = 1
        self._hasDragged = False


        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        self.pnl1 = wx.Panel(self, -1, style = wx.SIMPLE_BORDER)
        self.pnl2 = wx.Panel(self, -1, style = wx.NO_BORDER | wx.TAB_TRAVERSAL)
        self.pnl3 = wx.Panel(self, -1, style = wx.SIMPLE_BORDER | wx.TAB_TRAVERSAL, size=(self.PhotoMaxSizeSmall,self.PhotoMaxSizeSmall))
        self.pnl4 = wx.Panel(self, -1, style = wx.SIMPLE_BORDER | wx.TAB_TRAVERSAL)
        hbox1.Add(self.pnl1, 1, wx.EXPAND | wx.ALL, 1)
        hbox2.Add(self.pnl2, 1, wx.EXPAND | wx.ALL, 1)
        hbox3.Add(self.pnl3, 1, wx.EXPAND | wx.ALL, 1)
        hbox5.Add(self.pnl4, 1, wx.EXPAND | wx.ALL, 1)
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox3 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(hbox1, 1, wx.EXPAND | wx.ALL, 1)
        vbox1.Add(hbox2, 1, wx.EXPAND | wx.ALL, 1)
        vbox2.Add(hbox3, 1, wx.EXPAND | wx.ALL, 1)
        vbox3.Add(hbox5, 1, wx.EXPAND | wx.ALL, 1)
        hbox4.Add(vbox1, 2, wx.EXPAND | wx.ALL, 1)
        hbox4.Add(vbox2, 3, wx.EXPAND | wx.ALL, 1)
        hbox4.Add(vbox3, 1, wx.EXPAND | wx.ALL, 1)
        
        #wx.Button(self.pnl1,101 , "Plot", pos = (5,115))
        self.CloseGraph = wx.Button(self.pnl1, 102, "Close graph", pos = (5,180))
        wx.Button(self.pnl1, 103, "Hilbert", pos = (5,5))
        wx.Button(self.pnl1, 104, "Circos", pos = (5,40))
        wx.Button(self.pnl1, 106, "Close Program", pos = (170,250))
        wx.Button(self.pnl1, 108, "Convert vcf to csv", pos = (5,75))
        wx.Button(self.pnl1, 109, "Hilbert curve own data", pos = (5,110))
        wx.Button(self.pnl1, 110, "Change Picture", pos = (170,40))
        btn = wx.Button(self.pnl1, 111,  "Zoom on", pos = (170,5))
        wx.Button(self.pnl1, 111, "Drawline", pos = (170,75))
        self.pic = wx.Button(self.pnl1, 105, "Show Pic", pos = (5,145))
        self.delimg = wx.Button(self.pnl1, 107, "Delete Circos img", pos = (170,145))
        
        
        
        self.photoTxt = wx.TextCtrl(self.pnl1, size=(200,-1),pos = (5,215))
        wx.StaticText(self.pnl4,label = "Info:",pos = (5,5))
        self.infotext = wx.StaticText(self.pnl4,label = "",pos = (5,35))
        

        self.Bind(wx.EVT_BUTTON, self.ShowPlot, id = 101)
        self.Bind(wx.EVT_BUTTON, self.Closedev, id = 102)
        self.Bind(wx.EVT_BUTTON, self.Hilbert, id = 103)
        self.Bind(wx.EVT_BUTTON, self.Runcircos, id = 104)
        self.Bind(wx.EVT_BUTTON, self.Showimg, id = 105)
        self.Bind(wx.EVT_BUTTON, self.CloseProg, id = 106)
        self.Bind(wx.EVT_BUTTON, self.Delimg, id = 107)
        self.Bind(wx.EVT_BUTTON, self.Convertvcf, id = 108)
        self.Bind(wx.EVT_BUTTON, self.HilbertOwnData, id = 109)
        self.Bind(wx.EVT_BUTTON, self.onBrowse, id = 110)
        btn.Bind(wx.EVT_KEY_DOWN, self.zoom)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        #self.Bind(wx.EVT_BUTTON, self.Zoom, id = 111)
        self.SetSizer(hbox4)
        self.Centre()
        
        #wx.Image( graphicFilename, wx.BITMAP_TYPE_ANY ).ConvertToBitmap()

        img = wx.EmptyImage(self.PhotoMaxSizeSmall,self.PhotoMaxSizeSmall)
        self.imageCtrl = wx.StaticBitmap(self.pnl2, wx.ID_ANY,
                                         wx.BitmapFromImage(img),pos = (0,0))
        self.img = img
        img2 = wx.EmptyImage(self.PhotoMaxSizeBig,self.PhotoMaxSizeBig)
        self.imageCtrl2 = wx.StaticBitmap(self.pnl3, wx.ID_ANY,
                                         wx.BitmapFromImage(img2))
        self.img2 = img2
        self.img3 = wx.BitmapFromImage(img)
        self.imgBmap = wx.Image("/home/peter/Game/Textures/grass.jpg", wx.BITMAP_TYPE_ANY ).ConvertToBitmap()
        self.CloseGraph.Enable(0)
        self.topline = (self.imageCtrl.GetPosition()[0], self.imageCtrl.GetPosition()[0], self.imageCtrl.GetSize()[0],self.imageCtrl.GetPosition()[1])
        self.bottomline = (self.imageCtrl.GetPosition()[0], self.imageCtrl.GetSize()[1], self.imageCtrl.GetSize()[0],self.imageCtrl.GetSize()[1])
        self.leftline = (self.imageCtrl.GetPosition()[0], self.imageCtrl.GetPosition()[1], self.imageCtrl.GetPosition()[0],self.imageCtrl.GetSize()[1])
        self.rightline = (self.imageCtrl.GetSize()[0], self.imageCtrl.GetPosition()[1], self.imageCtrl.GetSize()[0],self.imageCtrl.GetSize()[1])
        self.imageCtrl2.Bind(wx.EVT_MOTION,self.info)
        self.imageCtrl2.Bind(wx.EVT_LEFT_DOWN,self.grabpicture)
        #self.imageCtrl2.Bind(wx.EVT_LEFT_UP,self.setpicture)

        if not os.path.isfile("/home/peter/circos-0.56/example/circos.svg"):
            self.pic.Enable(0)
            self.delimg.Enable(0)
            
            


    def info(self,event):
        #self.infotext.SetLabel("X = " + str(event.GetX()) + "\n" + "Y = " + str(event.GetY()))
        try:
            text = r('''
            hMat[{0},{1}]
            '''.format(event.GetX(),event.GetX()))
            self.infotext.SetLabel(str(text))
        except:
            pass
        if event.LeftIsDown():
            if self._hasDragged:
                self.dc2.Clear()
                self.dc2.DrawBitmapPoint(self.img4, (self.picturepos[0]-self.difx,self.picturepos[1]-self.dify))
            else:
                self._hasDragged= True
            self.difx = self.x-event.GetX()
            self.dify = self.y-event.GetY()
            
    
    def grabpicture(self,event):
        try:
            self.x = event.GetX()+self.difx
            self.y = event.GetY()+self.dify
        except:
            self.x = event.GetX()
            self.y = event.GetY()

        #self.dc2.DrawBitmapPoint( self.img4, (self.picturepos[0],self.picturepos[1]))
        
    
    #def setpicture(self,event):
    #    self.dc2.Clear()
    #    difx = self.x - event.GetX()
    #    dify = self.y - event.GetY()
    #    self.dc2.DrawBitmapPoint(self.img4, (self.picturepos[0]-difx,self.picturepos[1]-dify))
        
        


    def Zoom(self, event):
        h = self.img2.GetHeight()
        w = self.img2.GetWidth()
        newWidth = int(round(float(w) * self.scale))
        newHeight = int(round(float(h) * self.scale))
        
        self.img2.Rescale(newWidth, newHeight)
        #self.manageScrollbars(newWidth, newHeight, scale)
        #self.SetScrollbars(10, 10, newWidth/10, newHeight/10)
        self.display2()
    
    def display2(self):
        if self.img2:
            dc = wx.ClientDC(self)
            self.PrepareDC(dc)
            self.bitmap = self.img2.ConvertToBitmap()
            dc.DrawBitmap(self.bitmap, 0,0)
            
    
    def OnPaint(self, event):
        self.scaletup = 1
        self.picturepos = [0,0]
        self.img4 = wx.BitmapFromImage(self.img2)
        self.img3 = wx.BitmapFromImage(self.img)
        self.dc2 = wx.PaintDC(self.pnl3)
        self.dc = wx.PaintDC(self.pnl2)
        self.dc.Clear()
        self.dc2.Clear()
        self.dc.DrawBitmapPoint( self.img3, (0,0))
        self.dc2.DrawBitmapPoint( self.img4, (0,0))
        self.dc.SetPen(wx.Pen(wx.RED, 1))
        self.dc.DrawLine(self.topline[0],self.topline[1],self.topline[2],self.topline[3])
        self.dc.DrawLine(self.bottomline[0],self.bottomline[1],self.bottomline[2],self.bottomline[3])
        self.dc.DrawLine(self.leftline[0],self.leftline[1],self.leftline[2],self.leftline[3])
        self.dc.DrawLine(self.rightline[0],self.rightline[1],self.rightline[2],self.rightline[3])
        self.drawline = 0
        event.Skip()
            
            
    def draw(self,event):
        dc = wx.ClientDC(self)
        dc.DrawLine(400, 400, 190, 60)



    def zoom(self,event):
        if event.GetKeyCode() == 388 or event.GetKeyCode() == 61:
            self.dc.Clear()
            self.dc2.Clear()
            W = float(self.img2.GetWidth())
            H = float(self.img2.GetHeight())
            self.img2 = self.img2.Scale(W+5*W/self.img.GetWidth(),H+5*H/self.img.GetHeight())
            self.img4 = wx.BitmapFromImage(self.img2)
            #self.scaletup += 0.02*1.66
            #print self.scaletup
            #self.dc2.SetUserScale(self.scaletup,self.scaletup)
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
                    self.dc.DrawBitmapPoint( self.img3, (0,0))
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


    def ShowPlot(self, event):
        '''
        This function wil extract the values (self.x1, selfx2, self.y1, self.y2) from the gui, calls :class:`processes.Rplot()` and give the values as parameters.
        
        :var x1: `int <http://docs.python.org/library/functions.html#int>`_
        :var x2: `int <http://docs.python.org/library/functions.html#int>`_
        :var y1: `int <http://docs.python.org/library/functions.html#int>`_
        :var y2: `int <http://docs.python.org/library/functions.html#int>`_      
        '''
        try:
            x1 = int(self.x1.GetValue())
            x2 = int(self.x2.GetValue())
            y1 = int(self.y1.GetValue())
            y2 = int(self.y2.GetValue())
            processes.Rplot(x1,x2,y1,y2)
            self.CloseGraph.Enable(1)
        except:
            dlg = wx.MessageDialog(self,"Please put a number at X1,X2,Y1 and Y2","",wx.OK|wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def Hilbert(self, event):
        '''
        Runs the hilbertGUI in `R_V2.10.1 <http://www.r-project.org/>`_ (pipeline: `RPy2_V2.0.8 <http://rpy.sourceforge.net/rpy2.html>`_ ) by calling :class:`processes.Hilbert()`
        '''
        processes.Hilbert()
        self.photoTxt.SetValue("temp/HGui.png")
        self.onView()
        #self.CloseGraph.Enable(1)

    def Runcircos(self,event):
        '''
        Runs the program `Circos <http://www.circos.ca/>`_ by calling :class:`processes.Circos()`
        
        :var dlg: MessageDialog
        '''
        dlg = wx.MessageDialog(None, 'Circos is Running please wait')
        dlg.ShowModal()
        processes.Circos(self)
        if os.path.isfile("/home/peter/circos-0.56/example/circos.svg"):
            self.pic.Enable(1)
        #self.image = wx.Image('/home/peter/circos-0.56/example/circos.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        #wx.StaticBitmap(self.sw, -1, self.image)
        #self.sw.SetScrollbars(20,20,55,40)
        
    def Showimg(self,event):
        '''
        Presents the svg picture made by `Circos <http://www.circos.ca/>`_ in the standard webbrowser
        '''
        processes.ShowCircos()

    def Closedev(self, event):
        '''
        Closes the graph made by `R_V2.10.1 <http://www.r-project.org/>`_
        '''
        r('dev.off()')
        self.CloseGraph.Enable(0)


    def CloseProg(self,event):
        '''
        Close the program by using :class:`sys.exit()`
        '''
        sys.exit()
        
    def Delimg(self,event):
        '''
        Whis function will delete the iamge created by `Circos <http://www.circos.ca/>`_
        
        :var dlg: MessageDialog
        
        '''
        dlg = wx.MessageDialog(self, 'Are you sure you want to delete file?', 'Please Confirm', wx.YES_NO |
                wx.NO_DEFAULT | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            os.remove('/home/peter/circos-0.56/example/circos.svg')
            if not os.path.isfile("/home/peter/circos-0.56/example/circos.svg"):
                self.pic.Enable(0)
                self.delimg.Enable(0)
                
    def Convertvcf(self,event):
        '''
        This funtion will convert `vcf <http://www.1000genomes.org/wiki/Analysis/Variant%20Call%20Format/vcf-variant-call-format-version-41>`_  files to `csv <http://en.wikipedia.org/wiki/Comma-separated_values>`_ files by using the class: :class:`processes.Converter()`
        
        :var dlg: MessageDialog
        :var path: string
        :var path2: string
        '''
        dlg = wx.DirDialog(self, "Choose the folder with *.vcf files", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            dlg2 = wx.DirDialog(self, "Choose the folder to save the *.csv files", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
            if dlg2.ShowModal() == wx.ID_OK:
                path2 = dlg2.GetPath()
                processes.Converter(path,path2)
            dlg2.Destroy()
        dlg.Destroy()
        
    def HilbertOwnData(self,event):
        '''
        Calls the :class:`processes.HilbertOwn()` class which uses a csv file location as parameter
        '''
        dlg = wx.FileDialog(self, "Choose csv file",os.getcwd(), "","*.csv",wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.CloseGraph.Enable(1)
            path = dlg.GetPath()
            processes.HilbertOwn(path)


    def onBrowse(self, event):
        """
        Browse for file
        """
        wildcard = "JPEG files (*.jpg)|*.jpg|PNG files(*.png)|*.png|GIF files(*.gif)|*.gif"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoTxt.SetValue(dialog.GetPath())
        dialog.Destroy()
        self.onView()
 
    def onView(self):
        filepath = self.photoTxt.GetValue()
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW2 = self.PhotoMaxSizeBig
            NewH2 = self.PhotoMaxSizeBig * H / W
            NewW = self.PhotoMaxSizeSmall
            NewH = self.PhotoMaxSizeSmall * H / W
        else:
            NewH = self.PhotoMaxSizeSmall
            NewW = self.PhotoMaxSizeSmall * W / H
            NewW2 = self.PhotoMaxSizeBig
            NewH2 = self.PhotoMaxSizeBig * W / H
        try:
            img2 = img.Scale(r("nrow(hMat)")[0],r("nrow(hMat)")[0])
        except:
            print "fail"
            pass
        img = img.Scale(NewW,NewH)
        self.img2 = img2
        self.img = img
        self.drawline = 1
        self.topline = (self.imageCtrl.GetPosition()[0], self.imageCtrl.GetPosition()[0], self.imageCtrl.GetSize()[0],self.imageCtrl.GetPosition()[1])
        self.bottomline = (self.imageCtrl.GetPosition()[0], self.imageCtrl.GetSize()[1], self.imageCtrl.GetSize()[0],self.imageCtrl.GetSize()[1])
        self.leftline = (self.imageCtrl.GetPosition()[0], self.imageCtrl.GetPosition()[1], self.imageCtrl.GetPosition()[0],self.imageCtrl.GetSize()[1])
        self.rightline = (self.imageCtrl.GetSize()[0], self.imageCtrl.GetPosition()[1], self.imageCtrl.GetSize()[0],self.imageCtrl.GetSize()[1])
 
        #self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        #self.imageCtrl2.SetBitmap(wx.BitmapFromImage(img2))
        #self.pnl2.Refresh()
        
class MyApp(wx.App):
    '''
    Creates the frame
    :var frame: :class:`MyFrame()`
    '''
    def OnInit(self):
        frame = MyFrame(None, -1, "AMC Programm (Peter Admiraal)")
        frame.Show(True)
        frame.Centre()
        return True

app = MyApp(0)
app.MainLoop()
