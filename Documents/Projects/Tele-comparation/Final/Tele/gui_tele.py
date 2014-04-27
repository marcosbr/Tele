# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
from PySide.QtCore import *
from PySide.QtGui import *
from obspy.core import UTCDateTime
import numpy as np
import graphics2

__appname__ = "Tele"

class Ui_Dialog(object):
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 130)
        
        self.mapmarble = QtGui.QCheckBox(Dialog)
        self.mapmarble.setGeometry(QtCore.QRect(210, 80, 140, 20))
        self.mapmarble.setObjectName("mapmarble")
        
        self.mapfull = QtGui.QCheckBox(Dialog)
        self.mapfull.setGeometry(QtCore.QRect(210, 100, 180, 20))
        self.mapfull.setObjectName("mapfull")
        
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(17, 9, 560, 30))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.open_usgs = QtGui.QPushButton(self.widget)
        self.open_usgs.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        self.open_usgs.setObjectName("open_usgs")
        self.horizontalLayout.addWidget(self.open_usgs)
        self.open_usgs.clicked.connect(self.open_usg)
        
        self.open_data = QtGui.QPushButton(self.widget)
        self.open_data.setEnabled(True)
        self.open_data.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.open_data.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        self.open_data.setObjectName("open_data")
        self.horizontalLayout.addWidget(self.open_data)
        self.open_data.clicked.connect(self.open_obsis)
                
        self.coords = QtGui.QPushButton(self.widget)
        self.coords.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        self.coords.setObjectName("coords")
        self.horizontalLayout.addWidget(self.coords)
        self.coords.clicked.connect(self.open_coord)
        
        self.proc = QtGui.QPushButton(Dialog)
        self.proc.setGeometry(QtCore.QRect(210, 50, 180, 28))
        self.proc.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        self.proc.setObjectName("proc")
        self.proc.clicked.connect(self.processing)
        
        self.questionLabel = QtGui.QLabel()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Tele", None, QtGui.QApplication.UnicodeUTF8))
        self.proc.setText(QtGui.QApplication.translate("Dialog", "Processar", None, QtGui.QApplication.UnicodeUTF8))
        self.mapmarble.setText(QtGui.QApplication.translate("Dialog", "Mapa Simples", None, QtGui.QApplication.UnicodeUTF8))
        self.mapfull.setText(QtGui.QApplication.translate("Dialog", "Mapa Completo", None, QtGui.QApplication.UnicodeUTF8))
        self.open_usgs.setText(QtGui.QApplication.translate("Dialog", "Abrir Dado USGS", None, QtGui.QApplication.UnicodeUTF8))
        self.open_data.setText(QtGui.QApplication.translate("Dialog", "Abrir Dado OBSIS", None, QtGui.QApplication.UnicodeUTF8))
        self.coords.setText(QtGui.QApplication.translate("Dialog", "Abrir Coordenadas OBSIS", None, QtGui.QApplication.UnicodeUTF8))
    
    
    def open_usg(self):
        self.errorMessageDialog = QtGui.QErrorMessage(self)
        
        dir = "."
        filename_usgs = QFileDialog.getOpenFileName(self,__appname__+"Open File Dialog", dir=dir, filter="CSV Files (*.csv)")
                
        try:
            lines_usgs = open(filename_usgs[0], 'r').readlines()
            test=int(lines_usgs[1][0:4])
            self.filename_usgs = filename_usgs[0]
        except:
            self.errorMessageDialog.showMessage("Formato de Entrada incorreto: Arquivo do USGS")
    
    def open_obsis(self):
        self.errorMessageDialog = QtGui.QErrorMessage(self)
        dir = "."
        filename_obsis = QFileDialog.getOpenFileName(self,__appname__+"Open File Dialog", dir=dir, filter="Text Files (*.dat)")        
        
        if filename_obsis[0] != "":        
            obsis = open(filename_obsis[0], 'r').readlines()
            
            try:
                sta = obsis[1][0:4]
                day = int(obsis[1][5:8])
                hour = int(obsis[1][8:10])
                minu = int(obsis[1][10:12])
                seg = float(obsis[1][12:16])/10.0
                header=obsis[0]
                year = int(str(20)+header[4:])
                smonth = header[1:4] 
                if smonth == 'JAN':
                   month=1
                elif smonth == 'FEB':
                   month=2
                elif smonth == 'MAR':
                   month=3
                elif smonth == 'APR':
                   month=4
                elif smonth == 'MAY':
                   month=5
                elif smonth == 'JUN':
                   month=6
                elif smonth == 'JUL':
                   month=7
                elif smonth == 'AUG':
                   month=8
                elif smonth == 'SEP':
                   month=9
                elif smonth == 'OCT':
                   month=10
                elif smonth == 'NOV':
                   month=11
                elif smonth == 'DEC':
                   month=12
                self.lines_obsis = obsis
            except:
                self.errorMessageDialog.showMessage("Formato de Entrada incorreto: Arquivo do OBSIS")
    
    def open_coord(self):
        self.errorMessageDialog = QtGui.QErrorMessage(self)
        dir = "."
        filename_coor = QFileDialog.getOpenFileName(self,__appname__+"Open File Dialog", dir=dir, filter="Text Files (*.dat)")

        if filename_coor != "":
            try:
                lines_coord = open(filename_coor[0], 'r').readlines()
                for line_coord in lines_coord:
                    rsta = line_coord[2:6]
                    rlat = float(line_coord[6:13].replace('.',''))/10000
                    rslat = line_coord[13:14]
                    if  rslat == 'S':
                       rlat *= -1
                    rlon = float(line_coord[15:22].replace('.',''))/10000
                    rslon = line_coord[22:23]
                    if rslon == 'W':
                       rlon *= -1 
                self.filename_coord = filename_coor[0]
            except:
                 self.errorMessageDialog.showMessage("Formato de Entrada incorreto: Arquivo de Coordenadas!")
            
    def processing(self):
        from telef import *
        from obspy.core.util.geodetics import gps2DistAzimuth, kilometer2degrees
        from obspy.taup.taup import getTravelTimes
        
        
        filename_out, ok = QtGui.QInputDialog.getText(QtGui.QWidget(),"Arquivo de saida", "Entre com o nome: ")
        
        output = open(filename_out,'w')
        oheader1 = ['Estacao', 'Dia', 'H.Chegada', 'H. Origem','Latitude', ' Longitude', 'H', '    Mag', 'Tipo','Dist. Az.', 'Residuo','Regiao'.ljust(30)]
        oheader2 = ['       ','   ', ' hh:mm:ss ','hh:mm:ss ', ' (graus)', ' (graus) ', ' km', '   ','    ','    (graus)', '  (s)  ','      ' ] 
        output.write(self.lines_obsis[0][1:6])
        output.write('\n\n\n')        
            
        line=oheader1
        output.write('%7s %2s %7s %6s %6s %7s %3s %4s %2s %4s %3s %6s\n'%(line[0],line[1],line[2],line[3],line[4],line[5],line[6],
                                                                   line[7],line[8],line[9],line[10],line[11]))
        line=oheader2
        output.write('%7s %2s %7s %6s %6s %7s %3s %4s %2s %4s %3s %6s\n'%(line[0],line[1],line[2],line[3],line[4],line[5],line[6],
                                                                   line[7],line[8],line[9],line[10],line[11]))
        output.write('\n')
        
        cnt=0; lres=[]; lcnt=[]; elats=[]; elons=[]; emags=[]
        stlats=[]; stlons=[]; edeps=[]
        
        lines_usgs = open(self.filename_usgs, 'r').readlines()       
        
        for line_obsis in self.lines_obsis[1:]:
            hdr_obsis=self.lines_obsis[0]
            iOBSIS = getObSis(line_obsis,hdr_obsis)
            coords = getCoord(self.filename_coord, iOBSIS[0])
            stlats.append(coords[0])
            stlons.append(coords[1])

            for line in lines_usgs[1:]:
                l = line.split(',')
                otime = UTCDateTime(l[0])
                ootime = l[0]
                if otime < iOBSIS[6]:
                    elat = float(l[1])
                    elon = float(l[2])
                    if l[3] == "": 
                        dep = 0.0
                    else:
                        dep = float(l[3])
                    mag = float(l[4])                            
                    magType = l[5]
                    net = l[10]
                    elats.append(elat)
                    elons.append(elon)
                    emags.append(mag)
                    edeps.append(dep)
                    place = [l[13],l[14]]
                    delta = gps2DistAzimuth(elat,elon,coords[0],coords[1])[0]
                    delta = kilometer2degrees(delta/1000.)
                    tt = getTravelTimes(delta, dep, model='iasp91')
                    text = "FIRST ARRIVAL\n"
                    first = tt[0]
                    if first['phase_name'] == 'P':
                        text += "%s: %.1f\n" % (first['phase_name'],first['time'])
                        arriv = UTCDateTime(otime) + first['time']
                        res = arriv-iOBSIS[6]
                        cnt += 1
                        lcnt.append(cnt)
                        lres.append(res)
                        hc=str(iOBSIS[2]).zfill(2)+':'+str(iOBSIS[3]).zfill(2)+':'+str(iOBSIS[4]).zfill(2)
                        ho=str(otime.time)
                        delta=str(delta)
                        res=str(res)
                        final = [iOBSIS[0],str(iOBSIS[1]).zfill(2),hc,ho[:10].zfill(8),str(elat).zfill(8),str(elon).zfill(9),str(dep).ljust(6),str(mag).ljust(3),str(magType).ljust(3),str(delta)[:5],res[:8].ljust(8),str(place).ljust(50)]
                        line=final
                        output.write('%7s %2s %7s %6s %6s %7s %3s %4s %2s %4s %3s %6s\n'%(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11]))
                        temp = [elat, elon, mag, str(iOBSIS[0]), coords[0], coords[1]]
                       
                    break
                    
        output.close()
         
        ares = np.array(lres)
        acnt = np.array(lcnt)
        graphics2.scatter(acnt,ares)
        
        if self.mapfull.checkState()  == QtCore.Qt.Checked:
            graphics2.plt_map_marble(elats,elons,emags,edeps,stlats,stlons)
        else:
            graphics2.plt_map(elats,elons,emags,edeps,stlats,stlons)
            

    
            
