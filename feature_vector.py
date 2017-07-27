from os import listdir
from os.path import isfile, join
import haversine as h
import math
from scipy.spatial import ConvexHull
import numpy as np
import matplotlib.pyplot as plt
import min_bounding_box as mbd

def Interpret(line):
	# id,time(date hh:mm:ss),x,y
	params=line.split(',')
	tid=params[0]
	cal=params[1]

	date=cal.split(' ')[0]
	ymd=date.split('-')
	yy=int(ymd[0])
	mo=int(ymd[1])
	dd=int(ymd[2])

	time=cal.split(' ')[1]
	hms=time.split(':')
	hh=int(hms[0])
	mm=int(hms[1])
	ss=int(hms[2])

	x=float(params[2])
	y=float(params[3])

	record={'id':tid,'date':date,'time':time,\
			'dt':{'yy':yy,'mo':mo,'dd':dd,'hh':hh,'mm':mm,'ss':ss},\
			'x':x,'y':y}
	return record

def calcTime(start,end):
	# return seconds
	# time={'yy':yy,'mo':mo,'dd':dd,'hh':hh,'mm':mm,'ss':ss}
	import datetime
	d1=datetime.datetime(int(start['yy']), int(start['mo']), int(start['dd']), int(start['hh']), int(start['mm']), int(start['ss']))
	d2=datetime.datetime(end['yy'], end['mo'], end['dd'],end['hh'],end['mm'],end['ss'])
	# datetime.timedelta(seconds=1)
	return (d2-d1).seconds

def calculate_initial_compass_bearing(pointA, pointB):
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing
    
#directories = [f for f in listdir('data/')]
#onlyfiles = [f for f in listdir(file_path) if isfile(join(file_path, f))]

#print directories
#print onlyfiles

# 99494

#a = '8717,2008-02-02 13:30:47,116.39465,39.84351'
#b = '8717,2008-02-02 13:31:53,116.39439,39.84353'
#a = Interpret(a)
#b = Interpret(b)

#print a
#print b
#c = calcTime(a['dt'], b['dt'])
#print c

##############################################################
# clean trajectories of 01 directory
onlyfiles = [f for f in listdir('data/01/')]
onlyfiles_ = [f for f in listdir('data/02/')]

#print onlyfiles

#lgtlat_threshold = 0.002

#for file_n in onlyfiles:
#	with open('data/'+file_n,'w') as w:
#		with open('data/01/'+file_n, 'r') as f:
#			while True:
#				line1 = f.readline()
#				line2 = f.readline()
#				if not line2: break  # EOF
#				tmp1 = Interpret(line1)
#				tmp2 = Interpret(line2)
#				if abs(tmp1['x'] - tmp2['x']) <= lgtlat_threshold and abs(tmp1['y'] - tmp2['y']) <= lgtlat_threshold :
#					
#					tmp = line2
#					w.write(line1)
#					w.write(line2)
#				else:
#					print line1
#					print line2

#################################################
#feature_vector


#for file_n in onlyfiles:
#	with open('data/vectors','a') as w:
#		my_list = [line for line in open('data/01/'+file_n)]
#		sum_dist = .0
#		sum_angles = .0
#		a = Interpret(my_list[0])
#		b = Interpret(my_list[len(my_list)-1])
#		dist_total = h.Haversine((float(a['x']), float(a['y'])), (float(b['x']),float(b['y']))).meters
#		time = calcTime(a['dt'],b['dt'])
#		for i in range(0, len(my_list)-2):
#			m = Interpret(my_list[i])
#			s = Interpret(my_list[i+1])
#			sum_dist += h.Haversine([m['x'],m['y']],[s['x'],s['y']]).meters
#			sum_angles += calculate_initial_compass_bearing((m['x'],m['y']),(s['x'],s['y']))
#		move_hability = float(dist_total / sum_dist)
#		w.write( str(a['id'])+','+str(dist_total)+','+str(time)+','+str(sum_dist)+','+str(sum_angles)+','+str(move_hability)+'\n')


######################## Just 1 hour #################################

#for file_n in onlyfiles:
#	with open('data/vectors_hour','a') as w:
#		my_list = [line for line in open('data/01/'+file_n)]
#		sum_dist = .0
#		sum_angles = .0
#		a = Interpret(my_list[0])
#		b = Interpret(my_list[650])
#		dist_total = h.Haversine((float(a['x']), float(a['y'])), (float(b['x']),float(b['y']))).meters
#		time = calcTime(a['dt'],b['dt'])
#		points = []
#		for i in range(0, 651):
#			m = Interpret(my_list[i])
#			s = Interpret(my_list[i+1])
#			points.append([m['x'],m['y']])
#			sum_dist += h.Haversine([m['x'],m['y']],[s['x'],s['y']]).meters
#			sum_angles += calculate_initial_compass_bearing((m['x'],m['y']),(s['x'],s['y']))
#		if(sum_dist == 0):
#			move_hability = .0
#		else:
#			move_hability = float(dist_total / sum_dist)
#		hull = ConvexHull(points)
#		perimeter = hull.area
#		area = hull.volume
#		minxy = np.min(points, axis=0)
#		maxxy = np.max(points, axis=0)
#		width = maxxy[0] - minxy[0]
#		height = maxxy[1] - minxy[1]
#		aspect_ratio = (maxxy[0] - minxy[0])/ (maxxy[1] - minxy[1])
#		w.write( str(a['id'])+','+str(dist_total)+','+str(time)+','+str(sum_dist)+','+str(sum_angles)+','+str(move_hability)+\
#				','+str(perimeter)+','+str(area)+','+str(width)+','+str(height)+','+str(width/height)+'\n')

################################# DATA 02 300 POINTS ########################

for file_n in onlyfiles_:
	with open('data/vectors_hour_2','a') as w:
		my_list = [line for line in open('data/02/'+file_n)]
		print(file_n)
		sum_dist = .0
		sum_angles = .0
		a = Interpret(my_list[0])
		b = Interpret(my_list[299])
		dist_total = h.Haversine((float(a['x']), float(a['y'])), (float(b['x']),float(b['y']))).meters
		time = calcTime(a['dt'],b['dt'])
		points = []
		for i in range(0, 301):
			m = Interpret(my_list[i])
			s = Interpret(my_list[i+1])
			points.append([m['x'],m['y']])
			sum_dist += h.Haversine([m['x'],m['y']],[s['x'],s['y']]).meters
			sum_angles += calculate_initial_compass_bearing((m['x'],m['y']),(s['x'],s['y']))
		if(sum_dist == 0):
			move_hability = .0
		else:
			move_hability = float(dist_total / sum_dist)
		hull = ConvexHull(points)
		perimeter = hull.area
		area = hull.volume
		minxy = np.min(points, axis=0)
		maxxy = np.max(points, axis=0)
		width = maxxy[0] - minxy[0]
		height = maxxy[1] - minxy[1]
		aspect_ratio = (maxxy[0] - minxy[0])/ (maxxy[1] - minxy[1])
		w.write( str(a['id'])+','+str(dist_total)+','+str(time)+','+str(sum_dist)+','+str(sum_angles)+','+str(move_hability)+\
				','+str(perimeter)+','+str(area)+','+str(width)+','+str(height)+','+str(width/height)+'\n')

