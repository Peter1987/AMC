from rpy2.robjects import r
from threading import Thread
import os, commands, time

'''
module with classes used bij main.
'''

class Rplot():
    def __init__(self,x1,x2,y1,y2):
        r('library("rggobi")')
        r('x1 = {0}'.format(x1))
        r('x2 = {0}'.format(x2))
        r('y1 = {0}'.format(y1))
        r('y2 = {0}'.format(y2))
        r('x = c(x1,x2)')
        r('y = c(y1,y2)')
        r('ggobi(x,y)')
        
        

class Hilbert():
    def __init__(self):
        r('''library( HilbertVisGUI )
        vec <- makeRandomTestData( )
        #pushViewport( viewport( layout=grid.layout( 2, 2 ) ) )
        #for( i in 1:4 ) {
        #    pushViewport( viewport(
        #        layout.pos.row=1+(i-1)%/%2, layout.pos.col=1+(i-1)%%2 ) )
        #    plotHilbertCurve( i, new.page=FALSE )
        #    popViewport( )
        #}
        l = log(length(vec),4)
        hMat <- hilbertImage( vec ,l)
        png("temp/HGui.png",width=6+2/3, height=6+2/3, units="in", res=600)
        palettePos = colorRampPalette(c("white", "red"))(300)
        paletteNeg = colorRampPalette(c("white", "blue"))(300)
        p <- levelplot(hMat,col.regions = c(rev(paletteNeg), palettePos)) 
        grid.newpage() 
        pushViewport(viewport(xscale = p$x.limits, yscale = p$y.limits)) 
        do.call(panel.levelplot, trellis.panelArgs(p, 1)) 
        showHilbertImage( hMat )
        dev.off()
        #showHilbertImage( hMat, mode="EBImage" )''')

class ShowCircos():
    def __init__(self):
        from string import Template
        import webbrowser
        
        SVG ='<object data="/home/peter/circos-0.56/example/circos.svg" type="image/svg+xml"></object> '
        template = Template("<html>\n<body>\n<h1>\n${name}\n</h1>\n</body>\n</html>")
        #template = template.substitute(dict(name='Dinsdale'))
        template = template.substitute(dict(name=SVG))
        page = open('test.html','w')
        page.write(str(template))
        page.close()
        webbrowser.open("test.html",new = 1)

class Converter(Thread):
    def __init__(self,path,path2):
        Thread.__init__(self)
        self.path = path
        self.path2 = path2
        self.start()
        
        
    def run(self):
        import shutil
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        path = self.path
        path2= self.path2
        files = []
        for i in os.listdir(path):
            files.append(i)
    
            n=0
            for i in files:
                vcf = open(path+"/"+files[n])
                vcflines = vcf.readlines()
                vcfl = ""
                j = 0
                try:
                    (os.mkdir(path2+"/temp"))
                except OSError:
                    pass
                for j in range(len(vcflines)):
                    if "#CHROM" in vcflines[j]:
                        vcflines[j] = vcflines[j].replace("#CHROM","CHROM")
                    vcfl = vcfl + vcflines[j]
                    j =+ 1
                w = open(path2+"/temp/"+files[n].replace("vcf","tmp"),"w")
                w.write(vcfl)
                w.close()
                n+=1
            n=0
            for i in files:
                r('csvfile = read.csv("{0}",header = TRUE,sep = "\\t",comment.char = "#")'.format(path2+"/temp/"+files[n].replace("vcf","tmp")))
                r('write.csv(csvfile,"{0}",row.names = FALSE,)'.format(path2+"/n"+files[n].replace("vcf","csv")))
                n += 1
            shutil.rmtree(path2+"/temp")
            
            
    


class HilbertOwn():
    def __init__(self,path):
        r('''library( HilbertVisGUI )
            data = read.csv("%s")
            qual = data$QUAL
            chrom = data$CHROM
            pos = data$POS
            n=1
            a = c()
            #for (i in 1:tail(pos,n=1)){
            #    if (pos[n]==i){
            #        a = append(a, qual[n])
            #        n=n+1
            #        }
            #    else{
            #        a = append(a, 0)
            #    }
            #}
            l = log(length(vec),4)
            hMat <- hilbertImage(a, level = l)
            #showHilbertImage( hMat )
            #showHilbertImage( hMat, mode="EBImage" )
            ''' % path)

class Circos(Thread):
    def __init__(self,parent):
        """Init Worker Thread Class."""
        self.parent = parent
        Thread.__init__(self)
        self.start()    # start the thread
 
    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        circospath = "../../circos-0.56/example/"
        os.chdir(circospath)
        commands.getoutput('../bin/circos -conf etc/circos.conf')
        time.sleep(5)
        
class bla4():
    def __init__(self):
        pass