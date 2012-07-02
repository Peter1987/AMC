'''
Created on May 21, 2012

@author: peter
'''

import vcf

class DataReader():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
        
    def SetPath(self,path):
        self.__path = path



    def Parser(self):
        self.__vcf = vcf.Reader(open(self.__path, 'rb'))
        self.__information = [[],[],[],[],[],[],[],[]]
        for record in self.__vcf:
            self.__information[0].append(record.CHROM)
            self.__information[1].append(record.POS)
            self.__information[2].append(record.ID)
            self.__information[3].append(record.REF)
            self.__information[4].append(record.ALT)
            self.__information[5].append(record.QUAL)
            self.__information[6].append(record.FILTER)
            self.__information[7].append(record.INFO)
    
    def GetVCF(self):
        return self.__vcf
        
    def GetCHROM(self):
        return self.__information[0]
    
    def GetPOS(self):
        return self.__information[1]
    
    def GetID(self):
        return self.__information[2]
    
    def GetREF(self):
        return self.__information[3]
    
    def GetALT(self):
        return self.__information[4]
    
    def GetQUAL(self):
        return self.__information[5]
    
    def GetFILTER(self):
        return self.__information[6]
    
    def GetINFO(self):
        return self.__information[7]
    
    def GetALL(self):
        return self.__information
    
    def GetINFONames(self):
        return self.__vcf.infos.keys()
    
    def GetInfoValues(self):
        return self.__vcf.infos.values()
    
    def GetInfoType(self):
        return self.__vcf.infos.values()[3]
    