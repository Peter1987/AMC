import wx, vcf

class MyFrame(wx.Frame):

    def __init__(self, parent, Id, title):
        wx.Frame.__init__(self, parent, Id, title, wx.DefaultPosition, wx.Size(1500, 650))
        
        
        self.timer = wx.Timer(self)
        
        
        self.pnl1 = wx.Panel(self, -1, style = wx.SIMPLE_BORDER)
        self.pnl2 = wx.Panel(self, -1, style = wx.SIMPLE_BORDER | wx.TAB_TRAVERSAL)
        self.pnl3 = wx.Panel(self, -1, style = wx.SIMPLE_BORDER | wx.TAB_TRAVERSAL)
        
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        vbox1 = wx.BoxSizer(wx.VERTICAL)


        hbox1.Add(self.pnl1, 1, wx.EXPAND | wx.ALL, 1)
        hbox2.Add(self.pnl2, 1, wx.EXPAND | wx.ALL, 1)
        hbox3.Add(self.pnl3, 1, wx.EXPAND | wx.ALL, 1)
        
        
        self.pnl1openbutton = wx.Button(self.pnl1,100,"Open VCF",pos = (5,5))
        self.pnl1filenamectrl = wx.TextCtrl(self.pnl1,-1,"",pos = (5,40),size = (500,-1))
        self.pnl1helpbutton = wx.Button(self.pnl1,101,"help",pos = (125,5))
        
        
        self.pnl2checkbox1 = wx.CheckBox(self.pnl2,212,"Chromosome",pos = (5,5))
        self.pnl2checkbox2 = wx.CheckBox(self.pnl2,-1,"Postion",pos = (5,35))
        self.pnl2checkbox3 = wx.CheckBox(self.pnl2,-1,"ID",pos = (5,65))
        self.pnl2checkbox4 = wx.CheckBox(self.pnl2,-1,"Ref Base",pos = (5,95))
        self.pnl2checkbox5 = wx.CheckBox(self.pnl2,-1,"ALt Base",pos = (5,125))
        self.pnl2checkbox6 = wx.CheckBox(self.pnl2,-1,"Quality",pos = (125,5))
        self.pnl2checkbox7 = wx.CheckBox(self.pnl2,-1,"Filter",pos = (125,35))
        self.pnl2checkbox8 = wx.CheckBox(self.pnl2,210,"Info",pos = (125,65))
        self.pnl2checkbox9 = wx.CheckBox(self.pnl2,213,"Samples",pos = (125,95))
        self.pnl2openbutton = wx.Button(self.pnl2,110,"Load",pos = (125,120))
        

        self.pnl3textbox1 = wx.TextCtrl(self.pnl3,-1,"",pos = (5,5),size = (1485,390), style = wx.TE_READONLY | wx.TE_AUTO_SCROLL | wx.TE_MULTILINE | wx.HSCROLL)
        
        
        vbox1.Add(hbox1, 1, wx.EXPAND | wx.ALL, 1)
        vbox1.Add(hbox2, 2, wx.EXPAND | wx.ALL, 1)
        vbox1.Add(hbox3, 5, wx.EXPAND | wx.ALL, 1)
        
        
        self.Bind(wx.EVT_BUTTON,self.LoadVCF, id = 100)
        self.Bind(wx.EVT_BUTTON,self.Help,id = 101)
        self.Bind(wx.EVT_BUTTON,self.ShowVCF,id = 110)
        self.Bind(wx.EVT_CHECKBOX,self.ShowINFO,id = 210)
        self.Bind(wx.EVT_CHECKBOX,self.ChromsShow, id = 212)
        self.Bind(wx.EVT_CHECKBOX,self.ShowFormat,id = 213)
        self.Bind(wx.EVT_TIMER,self.updatescreen,self.timer)
        self.timer.Start(16)
        
        
        self.SetSizer(vbox1)
        self.Centre()


    def updatescreen(self,event):
        
        if self.pnl1filenamectrl.GetValue() != "":
            self.pnl2checkbox1.Enable(1)
            self.pnl2checkbox2.Enable(1)
            self.pnl2checkbox3.Enable(1)
            self.pnl2checkbox4.Enable(1)
            self.pnl2checkbox5.Enable(1)
            self.pnl2checkbox6.Enable(1)
            self.pnl2checkbox7.Enable(1)
            self.pnl2checkbox8.Enable(1)
            self.pnl2checkbox9.Enable(1)
            self.pnl2openbutton.Enable(1)
        else:
            self.pnl2checkbox1.Enable(0)
            self.pnl2checkbox2.Enable(0)
            self.pnl2checkbox3.Enable(0)
            self.pnl2checkbox4.Enable(0)
            self.pnl2checkbox5.Enable(0)
            self.pnl2checkbox6.Enable(0)
            self.pnl2checkbox7.Enable(0)
            self.pnl2checkbox8.Enable(0)
            self.pnl2checkbox9.Enable(0)
            self.pnl2openbutton.Enable(0)
        
        
    def Help(self,event):

        vcf_reader = vcf.Reader(open(self.pnl1filenamectrl.GetValue(), 'rb'))
        self.helptext = ""
        for i in range(len(vcf_reader.infos.keys())):
            self.helptext += str(vcf_reader.infos.keys()[i]) + " : " + str(vcf_reader.infos.values()[i][3]) + "\n"
        dlg = wx.MessageDialog(self, self.helptext, 'Info', wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


    def ShowFormat(self,event):
        if self.pnl2checkbox9.GetValue() == True:
            self.shift = 0
            vcf_reader = vcf.Reader(open(self.pnl1filenamectrl.GetValue(), 'rb'))
            formats =  vcf_reader.formats.keys()
            self.pnl2formatcheckbox = []
            try:
                self.checkposx += 120
            except:
                self.checkposx = 485
            checkposy = 30
            n = 0
            for form in formats:
                self.pnl2formatcheckbox.append(wx.CheckBox(self.pnl2,-1,form,pos = (self.checkposx,5 + checkposy*n)))
                n += 1
                if n == 5:
                    n = 0
                    self.checkposx += 120
                    self.shift += 1
        else:
            for i in range(len(self.pnl2formatcheckbox)):
                self.pnl2formatcheckbox[i].Destroy()
            self.checkposx -= 120 * (self.shift + 1)
            
        

    def ChromsShow(self,event):

        Chroms = []
        altchroms = []
        vcf_reader = vcf.Reader(open(self.pnl1filenamectrl.GetValue(), 'rb'))
        for record in vcf_reader:
            if len(record.CHROM) <=5:
                Chroms.append(record.CHROM)
            else:
                altchroms.append(record.CHROM)
        chromset =  list(set(Chroms))
        altchroms =  list(set(altchroms))
        for i in range(len(chromset)):
            if len(chromset[i]) == 4 and "M" not in chromset[i] and "X" not in chromset[i] and "Y" not in chromset[i]:
                chromset[i] = chromset[i].replace("chr","chr0")
        wx.StaticText(self.pnl2,-1,str(vcf_reader.samples[0]),pos = (240,5))
        self.Chrombox = wx.ComboBox(self.pnl2,210,sorted(chromset)[0],choices = sorted(chromset),pos = (245,35), style=wx.CB_READONLY)


    def ShowINFO(self,event):
        if self.pnl2checkbox8.GetValue() == True:
            self.shift = 0
            self.pnl2infocheckbox = []
            vcf_reader = vcf.Reader(open(self.pnl1filenamectrl.GetValue(), 'rb'))
            try:
                self.checkposx += 120
            except:
                self.checkposx = 485
            checkposy = 5
            info = []
            n = 0
            for i in vcf_reader.infos.keys():
                info.append(i)
                print self.checkposx,checkposy+n*30
                self.pnl2infocheckbox.append(wx.CheckBox(self.pnl2,-1,i,pos = (self.checkposx,checkposy+n*30)))
                n += 1
                if n == 5:
                    n = 0
                    self.checkposx += 120
                    self.shift += 1
        else:
            for i in range(len(self.pnl2infocheckbox)):
                self.pnl2infocheckbox[i].Destroy()
            self.checkposx -= 120 * (self.shift + 1)
            

    def LoadVCF(self,event):
        
        wildcard = "VCF files (*.vcf)|*.vcf"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.pnl1filenamectrl.SetValue(dialog.GetPath())
        dialog.Destroy()
            

    def ShowVCF(self,event):
        
        n = 0
        self.showtext = ""
        vcf_reader = vcf.Reader(open(self.pnl1filenamectrl.GetValue(), 'rb'))
        self.showtext += str(vcf_reader.samples[0])+":\n"
        helptext = ""
        for record in vcf_reader:
            try:
                if str(record.CHROM) == self.Chrombox.GetValue():
                    print "yes"
                else:
                    print "no"
            except:
                pass
            if self.pnl2checkbox1.GetValue() == True:
                self.showtext += "{0:>10}".format(record.CHROM)+"\t"
            if self.pnl2checkbox2.GetValue() == True:
                self.showtext += "{0:>10}".format(record.POS)+"\t"
            if self.pnl2checkbox3.GetValue() == True:
                self.showtext += "{0:>10}".format(record.ID)+"\t"
            if self.pnl2checkbox4.GetValue() == True:
                self.showtext += "{0:>10}".format(record.REF)+"\t"
            if self.pnl2checkbox5.GetValue() == True:
                self.showtext += "{0:>10}".format(record.ALT)+"\t"
            if self.pnl2checkbox6.GetValue() == True:
                self.showtext += "{0:>10}".format(record.QUAL)+"\t"
            if self.pnl2checkbox7.GetValue() == True:
                self.showtext += "{0:>10}".format(record.FILTER)+"\t"
            if self.pnl2checkbox8.GetValue() == True:
                for i in self.pnl2infocheckbox:
                    if i.GetValue() == True:
                        try:
                            self.showtext += str(i.GetLabel()) + " : " + str(record.INFO[i.GetLabel()]) +"\t"
                        except:
                            pass
            if self.pnl2checkbox9.GetValue() == True:
                for j in vcf_reader.samples:
                    self.showtext += str(j) + " : "
                    print str(j)
                    for i in self.pnl2formatcheckbox:
                        if i.GetValue() == True:
                            try:
                                self.showtext += str(i.GetLabel()) + " : " + str(record.genotype(str(j))[str(i.GetLabel())])
                            except:
                                print "bla"
            self.showtext += "\n"
            n += 1
            if n == 100:
                break
        formats = record.FORMAT.split(":")
        self.helptext = helptext
        self.pnl3textbox1.SetValue(self.showtext)

        
class MyApp(wx.App):
    
    def OnInit(self):
        
        frame = MyFrame(None, -1, "VCF Show (Peter Admiraal)")
        frame.Show(True)
        return True

app = MyApp(0)
app.MainLoop()

