import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path

def histogram(data,xlabel):
    fig,ax = plt.subplots()
    n,bins = np.histogram(data,25)

    left = np.array(bins[:-1])
    right = np.array(bins[1:])
    bottom = np.zeros(len(left))
    top = bottom + n

    XY = np.array([[left,left,right,right],[bottom,top,top,bottom]]).T
    barpath = path.Path.make_compound_path_from_polys(XY)

    patch = patches.PathPatch(barpath, facecolor='green', edgecolor='gray',alpha=0.8)
    ax.add_patch(patch)
    
    ax.set_xlim(left[0],right[-1])
    ax.set_ylim(bottom.min(),top.max())
    ax.set_ylabel('Frequency')
    ax.set_xlabel(xlabel)
    plt.show()


def roseDgr(dat_len,dat_azm):
    N=np.size(dat_len)
    azm=dat_azm
    radius=dat_len
    width=azm*np.pi/180
  
    ax = plt.subplot(111, polar=True)
    bars = ax.bar(azm,radius,width=width,bottom=0.0)

    for r,bar in zip(radius,bars):
        bar.set_facecolor(plt.cm.jet(r/10.))
        bar.set_alpha(0.5)

    plt.show()

def scatter(x,y):
    from matplotlib.pylab import figure,show, setp
    fig=figure()
    ax1 = fig.add_subplot(1,1,1)
    xmax=np.max(x)+0.5
    markerline, stemline, baseline = ax1.stem(x,y,'-.')
    setp(markerline, 'markerfacecolor', 'b')
    setp(baseline, 'color', 'r', 'linewidth', 2)
    ax1.set_xlabel('Evento')
    ax1.set_ylabel('Residuo (s)')
    ax1.set_xlim([0.5,xmax])
    show()

def plt_shp():
    from numpy import ma
    from mpl_toolkits.basemap import Basemap, cm
    from osgeo import gdal, ogr

    fig=plt.figure(figsize=(11,6))
    m=Basemap(llcrnrlon=-119, llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,projection='lcc',lat_1=33,lat_2=45,lon_0=-95)

    m.drawparallels(np.arange(20,71,10),labels=[1,0,0,0])
    m.drawmeridians(np.arange(-120,-40,10),labels=[0,0,0,1])
    m.drawcountries(linewidth=4)
    #fill the backgroun ( oceans)
    m.drawmapboundary(fill_color='aqua') 
    plt.show()


def plt_map(lats,lons,magnitudes, dep, stlats, stlons):
    from mpl_toolkits.basemap import Basemap
    import matplotlib as mpl
    import pylab as pl
     
    pl.figure(figsize=(32,16))
 
    dmax = 650
    dmin = 0
    step = 10
    mymap = mpl.colors.LinearSegmentedColormap.from_list('mycolors',['red','green','blue'])
    Z = [[0,0],[0,0],[0,0]]
    levels = range(dmin,dmax+step,step) 
    CS3 = plt.contourf(Z, levels,cmap=mymap)

    plt.clf()
    def get_maker_size(mag):
        min_marker_size = 1.5
        if mag < 4:
           size = min_marker_size
        elif mag < 5:
           size = min_marker_size*4
        elif mag < 6:
           size = min_marker_size*5
        elif mag < 7:
           size = min_marker_size*6
        elif mag < 8:
           size = min_marker_size*7
        else:
           size = min_marker_size*8
        return size


    def get_marker_color(magnitude):
        if magnitude < 60.0:
            return ('ro')
        elif magnitude < 300.0:
            return ('go')
        else:
            return ('bo')
    
    map = Basemap(projection='robin',resolution='l',area_thresh=1000.0,lat_0=60.,lon_0=-60.)
    map.drawcoastlines()
    map.drawcountries()
    map.fillcontinents(color='gray')
    #map.bluemarble()
    map.drawmapboundary()
    map.drawmeridians(np.arange(0,360,60), labels=[True,False,False,True])
    map.drawparallels(np.arange(-90,90,30), labels=[False,True,True,False]) #[left,right,top,bottom]
    
    st_marker_size = 7 
    for slon,slat in zip(stlons, stlats):
        sx,sy = map(slon,slat)
        ssize = st_marker_size
        map.plot(sx,sy,'b^',markersize=ssize)
    
    mu = (dmax+dmin)/2.
    Z = [dmin, (mu+dmin)/2.,(mu+dmax)/2., dmax] 
    #for lon,lat,mag, edep, z in zip(lons, lats, magnitudes,dep, Z):
    for lon,lat,mag, edep in zip(lons, lats, magnitudes,dep):
        x,y = map(lon,lat)
       # r=(float(z)-dmin)/(dmax-dmin)
       # g=0
       # b=1-r
       # msize = mag*min_marker_size
        msize = get_maker_size(mag)
        marker_string = get_marker_color(edep)
        map.plot(x,y,marker_string,markersize=msize)
       # map.plot(x,y,markerfacecolor=(r,g,b),markersize=msize)
    #plt.scatter(x,y,s=msize,c=edep,vmin=5,vmax=30)

    cb = plt.colorbar(CS3, shrink=.5, pad=.1, aspect=10)
    cb.set_label('Profundidade (km)')
    
    plt.show()

def plt_map_marble(lats,lons,magnitudes, dep, stlats, stlons):
    from mpl_toolkits.basemap import Basemap
    import matplotlib as mpl
    import pylab as pl
     
    pl.figure(figsize=(32,16))
 
    dmax = 650
    dmin = 0
    step = 10
    mymap = mpl.colors.LinearSegmentedColormap.from_list('mycolors',['red','green','blue'])
    Z = [[0,0],[0,0],[0,0]]
    levels = range(dmin,dmax+step,step) 
    CS3 = plt.contourf(Z, levels,cmap=mymap)

    plt.clf()
    def get_maker_size(mag):
        min_marker_size = 1.5
        if mag < 4:
           size = min_marker_size
        elif mag < 5:
           size = min_marker_size*4
        elif mag < 6:
           size = min_marker_size*5
        elif mag < 7:
           size = min_marker_size*6
        elif mag < 8:
           size = min_marker_size*7
        else:
           size = min_marker_size*8
        return size


    def get_marker_color(magnitude):
        if magnitude < 60.0:
            return ('ro')
        elif magnitude < 300.0:
            return ('go')
        else:
            return ('bo')
    
    map = Basemap(projection='robin',resolution='l',area_thresh=1000.0,lat_0=60.,lon_0=-60.)
    map.drawcoastlines()
    map.drawcountries()
    #map.fillcontinents(color='gray')
    map.bluemarble()
    map.drawmapboundary()
    map.drawmeridians(np.arange(0,360,60), labels=[True,False,False,True])
    map.drawparallels(np.arange(-90,90,30), labels=[False,True,True,False]) #[left,right,top,bottom]
    
    st_marker_size = 7 
    for slon,slat in zip(stlons, stlats):
        sx,sy = map(slon,slat)
        ssize = st_marker_size
        map.plot(sx,sy,'b^',markersize=ssize)
    
    mu = (dmax+dmin)/2.
    Z = [dmin, (mu+dmin)/2.,(mu+dmax)/2., dmax] 
    #for lon,lat,mag, edep, z in zip(lons, lats, magnitudes,dep, Z):
    for lon,lat,mag, edep in zip(lons, lats, magnitudes,dep):
        x,y = map(lon,lat)
       # r=(float(z)-dmin)/(dmax-dmin)
       # g=0
       # b=1-r
       # msize = mag*min_marker_size
        msize = get_maker_size(mag)
        marker_string = get_marker_color(edep)
        map.plot(x,y,marker_string,markersize=msize)
       # map.plot(x,y,markerfacecolor=(r,g,b),markersize=msize)
    #plt.scatter(x,y,s=msize,c=edep,vmin=5,vmax=30)

    cb = plt.colorbar(CS3, shrink=.5, pad=.1, aspect=10)
    cb.set_label('Profundidade (km)')
    
    plt.show()
