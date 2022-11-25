import os
import mysql.connector
import RPi.GPIO as GPIO
import datetime, time
import csv

GPIO.setmode(GPIO.BCM)
#GPIO.setup(25, GPIO.IN)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

product = 'VLOZ-117MS-0B'
count = 1
counting = 0

hostname = '192.168.75.172'
username = 'root'
password = ''
database = 'database_pi'

date_today = datetime.datetime.now()
month_first_day = date_today.replace(month=datetime.datetime.now().date().month, day=1, hour=8, minute=0, second=0, microsecond=0)
month_last_day = date_today.replace(month=datetime.datetime.now().date().month+1, day=1, hour=8, minute=0, second=0, microsecond=0)
month_first = datetime.datetime.now().date().month
month_last = datetime.datetime.now().date().month - 1

def insert_record(id, Date_Time, Product_Name,Count,Takt_time,start_time, end_time):
        query = "INSERT INTO a5 (id, Date_Time, Product_Name,Count,Takt_time,start_time, end_time) " \
                "VALUES (%s,%s,%s,%s,%s,%s,%s)"
        args = (id, Date_Time, Product_Name,Count,Takt_time,start_time, end_time)

        try:
            conn = mysql.connector.connect( host=hostname, user=username, passwd=password,database=database)
            cursor = conn.cursor()
            cursor.execute(query, args)
            conn.commit()
            
        except Exception as error:
            print(error)

        finally:
            cursor.close()
            conn.close()       

try:
    start = time.time()
    #s1 = time.time()
    starttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    while True:
       
        if GPIO.input(17) == 1:
            now = datetime.datetime.now()
            date = now.strftime('%Y-%m-%d %H:%M:%S')
            starttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            counting = counting + 1
            timenow = time.time()
            #t= round((time.time() - s1),0)
            takttime = round((timenow - start),2)
            #file.write(str(counting)+","+str(date)+","+str(product)+","+str(count)+","+str(takttime)+"\n")
            #file.flush()

            while GPIO.input(17) == 1:
                  time.sleep(0.1)
            endtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            start = time.time()
            #s1 = time.time()
            #takttime = (round((timenow - start),0) + t) 
            insert_record(str(counting), str(date), str(product), str(count), str(takttime), str(starttime), str(endtime))
            if month_first_day <= date_today < month_last_day:
               csv_name = '/home/fujikura/Desktop/QtGUI/Database_pi/'+ str(month_first) +".csv"
            else:
               csv_name = '/home/fujikura/Desktop/QtGUI/Database_pi/'+ str(month_last) +".csv"  
        
            file = open(csv_name, "a") 
            file.write(str(counting)+","+str(date)+","+str(product)+","+str(count)+","+str(takttime)+"\n")
            file.flush()
          
            print("*" * 60)
            print("Object is detect.")
            print(('Counter = %s') % counting)
            #print("Counter : " + str(date)+","+str(product)+","+str(count))
            print(str(date)+","+str(product)+","+str(count)+","+str(takttime)+","+str(starttime)+","+str(endtime))
            print("time between detections", str(takttime), "seconds")
            print("Mysql Updated")
            print("*" * 60)
            print(endtime,"Time End")
            print(starttime,"Time Start")
            
            #print("Object is not detect.")
            #print("Counting = 0")       
except KeyboardInterrupt:
    GPIO.cleanup()
    


