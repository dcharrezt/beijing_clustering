from urllib2 import urlopen
from pylab import imshow, imread, show

lon = [49.5,50.35]
lat = [18.6,20.2]
scale = 700000

print "Downloading map... "
tries = 0
url = None
while tries < 60:
    tries += 1
    print 'Try {}...'.format(tries)
    try:
        url = urlopen('http://parent.tile.openstreetmap.org/cgi-bin/export?'
                      'bbox={lat1:.2f},{lon1:.2f},{lat2:.2f},{lon2:.2f}&'
                      'scale={scale:d}&format=png'.format(lat1=lat[0],
                      lat2=lat[1],
                      lon1=lon[0],
                      lon2=lon[1],
                      scale=scale))
    except HTTPError:
        sleep(5)
        continue
    else:
        print 'Map successfully downloaded.'
        break

if url is None:
    print 'Failed to download a map.'
else:
    m = imread(url)
    imshow(m, extent=lat+lon, aspect='equal')
    show()
