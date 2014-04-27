#Functions used in tele.py

from obspy.core import UTCDateTime

def getCoord(filename_coord,sta):
        lines_coord = open(filename_coord, 'r').readlines()
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
            if rsta == sta:
               coord = [rlat, rlon]
               break 
        return coord

def getTime(otime):
    year=int(otime.split('T')[0].split('-')[0])
    month=int(otime.split('T')[0].split('-')[1])
    day=int(otime.split('T')[0].split('-')[2])
    hour=int(otime.split('T')[1].split('Z')[0].split(':')[0])
    minu=int(otime.split('T')[1].split('Z')[0].split(':')[1])
    seg=float(otime.split('T')[1].split('Z')[0].split(':')[2])
    return [year,month,day,hour,minu,seg]

def getObSis(line_obsis,header):
    sta = line_obsis[0:4]
    day = int(line_obsis[5:8])
    hour = int(line_obsis[8:10])
    minu = int(line_obsis[10:12])
    seg = float(line_obsis[12:16])/10.0
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

    tobsis = UTCDateTime(year,month,day,hour,minu,seg)
    return [sta,day,hour,minu,seg,year,tobsis]

def getUSGS(line):
    l = line.split(',')
    otime = UTCDateTime(l[0])
    elat = float(l[1])
    elon = float(l[2])
    if l[3] == "": 
	dep = 0.0
    else:
	dep = float(l[3])
    mag = float(l[4])
    magType= l[5]
    net = l[10]
    place = [l[11],l[12]]
    return [otime,elat,elon,dep,mag,magType,net,place]

def writeFile(line,output):
            f = open(output,'a')
            f.write('%7s %2s %7s %6s %6s %7s %3s %4s %2s %4s %3s %6s\n' %(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11]))

