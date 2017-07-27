#!/usr/bin/python
import psycopg2
from config import config
from os import listdir
from os.path import isfile, join
 
def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
 
        # create a cursor
        cur = conn.cursor()
        
 # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
 
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
     # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def insert_traj_list(traj_list):

    sql = '''INSERT INTO trajectories(id, geom, times, lgt, lat)
             VALUES(%s, ST_SetSRID(ST_MakePoint(%s, %s),4326), %s, %s, %s);'''
             

    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql,traj_list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            
def get_car_traj(n_id):
    """ query data from the vendors table """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT * FROM taxis_beijin WHERE id = '%s'" %(n_id))
        print("The number of parts: ", cur.rowcount)
        row = cur.fetchone()
 
        while row is not None:
            print(row)
            row = cur.fetchone()
 
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
#    conn = psycopg2.connect(dsn)
#    cur = conn.cursor()

# insert_traj_list([
#    (1, 116.51172, 39.92123, '2008-02-02 15:36:08',),
#    (1, 116.51627, 39.91034, '2008-02-02 15:56:08',)
#])
#get_car_traj(1)
	traj_list = []
	directory_path = 'data/01/'
	onlyfiles = [f for f in listdir(directory_path)]
	for i in onlyfiles:
		print i
		with open(directory_path+i, 'r') as f:
			for line in f:
				tmp = (line.rstrip('\n').rstrip('\r').rsplit(','))
				traj_list.append((tmp[0], tmp[2], tmp[3], tmp[1], tmp[2], tmp[3]))
	insert_traj_list(traj_list)

#	path = "/home/ms/DB/beijing_cabs/data/01/366.txt"
#	
#	




    
    
