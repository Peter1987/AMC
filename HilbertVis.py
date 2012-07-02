from rpy2.robjects import r

class Hilbert:
    def __init__(self,data):
        r('a = c()')
        for i in data:
            r('a = append(a, {0})'.format(i))
        r('''library( HilbertVisGUI )
        hMat <- hilbertImage(a,7)
        res = (2^7)*8
        png("temp/HGui.png",width=6, height=6, units="in", res=res/6)
        palettePos = colorRampPalette(c("white", "red"))(300)
        paletteNeg = colorRampPalette(c("white", "blue"))(300)
        p <- levelplot(hMat,col.regions = c(rev(paletteNeg), palettePos))
        grid.newpage()
        pushViewport(viewport(xscale = p$x.limits, yscale = p$y.limits))
        do.call(panel.levelplot, trellis.panelArgs(p, 1))
        #showHilbertImage( hMat )
        dev.off()
        #showHilbertImage( hMat, mode="EBImage" )''')
        self.__size = 7
        
    def GetSize(self):
        return self.__size
