#!/usr/bin/python
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

import time
from adxl345 import ADXL345 #vin=5v pin2
import serial

port=serial.Serial("/dev/ttyAMA0",9600,timeout=3.0)

import MySQLdb
db=MySQLdb.connect("localhost", "cinfo", "root", "new") 


count=1

cur=db.cursor()
import smbus
import time
import math
power_mgmt1=0x6b
power_mgmt2=0x6c

   

adxl345 = ADXL345()


IR=24			#pin no.18
buzz=25			#pin no.22 
crash=12     #pin 32
GPIO.setup(buzz,GPIO.OUT)

port=serial.Serial("/dev/ttyAMA0",9600,timeout=3.0)


GPIO.setup(crash,GPIO.IN) #CRASH

GPIO.setup(23,GPIO.OUT)
motor=23
GPIO.output(motor,GPIO.HIGH)

GPIO.setup(IR,GPIO.IN)
GPIO.setup(buzz,GPIO.OUT)
def cras():
	if GPIO.input(crash):
  		print'NOTHING '
		GPIO.output(motor,GPIO.LOW)
		GPIO.cleanup()
		
 		
	else:
 		
		print'ACCIDENT'
		try:
			
	
		
			
			GPIO.output(motor,GPIO.LOW)
		        GPIO.cleanup()
			

			port=serial.Serial("/dev/ttyAMA0",9600,timeout=3.0)

 
 			#print'ACCIDENT'
	
			rcvdfile=port.read(1200)
			pos1=rcvdfile.find("$GPRMC")
			pos2=rcvdfile.find("\n",pos1)
			loc=rcvdfile[pos1:pos2]
			data=loc.split(',')
			pos11=rcvdfile.find("$GPGGA")
			pos22=rcvdfile.find("\n",pos11)
			loc1=rcvdfile[pos11:pos22]
			data1=loc1.split(',')
			if (data[2]=='V'):
					print'no location found'
			else:
					#print"UTC time="+data[1]+"UTC date="+data[9]
					gps_time=float(data[1])
					gps_date=float(data[9])
					gps_hour=int(gps_time/10000.0)
					gps_min=gps_time%10000.0
					gps_sec=gps_min%100.0
					gps_min=int(gps_min/100.0)
					gps_sec=int(gps_sec)
					gps_dd=int(gps_date/10000.0)
					gps_mm=gps_date%10000.0
					gps_yy=gps_mm%100.0
					gps_mm=int(gps_mm/100.00)
					gps_yy=int(gps_yy)
		
					print 'time=',gps_hour,':',gps_min,':',gps_sec
					print 'date=',gps_dd,'/',gps_mm,'/',gps_yy
		
					print "Latitude="+data[3]+data[4]
					print "Longitude="+data[5]+data[6]
					print "Speed="+data[7]
					print "Course="+data[8]
					print "\n"
					gps_time_gga=float(data1[1])
					gps_hour_gga=int(gps_time_gga/10000.0)
					gps_min_gga=gps_time_gga%10000.0
					gps_sec_gga=gps_min_gga%100.0
					gps_min_gga=int(gps_min_gga/100.0)
					gps_sec_gga=int(gps_sec_gga)
		
					print 'time=',gps_hour_gga,':',gps_min_gga,':',gps_sec_gga
					print "Latitude="+data1[2]+data1[3]
					print "Longitude="+data1[4]+data1[5]
					print "Satellites used="+data1[7]
					print "Altitude="+data1[9]
					print "\n"
		
					f=open('gps','w')
					f.write("Latitude="+data[3]+data[4])
					f.write("Longitude="+data[5]+data[6])
					f.write("Speed="+data[7])
					f.write("Course="+data[8])
        		print "GSM SIM9600\n"
			print"AT to check operation"
			port.write('AT\r\n')
			rcv=port.read(20)
			print"GSM Working:"+rcv
	                                                      #while True:
			rcv=port.read(20)
	
			cur.execute("SELECT name,phoneNum FROM contact")
			f=open('gps','r')
			f.seek(0)
			g=f.read()
			print g
			for row in cur.fetchall():
				name=str(row[0])    #rows=no of attributes
				number=str(row[1])
				msg1="accident occured at"	
				msg2=g
				print"message passed to  "+name		        #keyin=raw_input("msg number:")
				port.write('AT+CMGS="'+number+'"\r\n')
				time.sleep(2)
				
				
				port.flushInput()
				port.flushOutput()
				port.write(msg1)
				port.write(msg2)
				time.sleep(2)
				port.write('\x1A\r\n')
				print port.read(50)
				port.flushInput()
				port.flushOutput()
				
		except:
			port.close()

def read_byte(adr):
		return bus.read_byte_data(address,adr)
def read_word(adr):
		high=bus.read_byte_data(address,adr)
		low=bus.read_byte_data(address,adr+1)
		val=(high<<8) + low
		return val
def read_word_2c(adr):
		val=read_word(adr)
		if (val >= 0x8000):
			return -((65535 - val) +1)
		else:
			return val
def dist(a,b):
		return math.sqrt((a*a)+(b*b))
def get_y_rotataion(x,y,z):
		radians= math.atan2(x,dist(y,x))
		return -math.degrees(radians)
def get_x_rotataion(x,y,z):
		radians= math.atan2(y,dist(x,z))
		return math.degrees(radians)
bus = smbus.SMBus(1)
address= 0x68
bus.write_byte_data(address, power_mgmt1,0)	
accel_xout= read_word_2c(0x3b)
accel_yout= read_word_2c(0x3d)
accel_zout= read_word_2c(0x3f) 

while True:

   	
   	
	axes = adxl345.getAxes(True)
	print "ADXL345 on address 0x%x:" % (adxl345.address)
	print "   x = %.3f" % ( axes['x'] )
	print "   y = %.3f" % ( axes['y'] )
	print "   z = %.3f" % ( axes['z'] )
	accel_xout1= read_word_2c(0x3b)
        accel_yout1=  read_word_2c(0x3d)
        accel_zout1=  read_word_2c(0x3f)
	
	
	if ((accel_zout-100<=accel_zout1<=accel_zout+100) or (accel_xout-100<=accel_xout1<=accel_xout+100) or (accel_yout-100<=accel_yout1<=accel_yout+100)):
		count=count+1
		print count
	else:
		count=1
		print "DRIVING"
	if(count==20):
		GPIO.output(buzz,GPIO.HIGH)
		time.sleep(2)
		GPIO.output(buzz,GPIO.LOW)
		count=1
	
        if GPIO.input(IR):
		p=0 	
		print "okay"
		GPIO.output(buzz,GPIO.LOW)
	else:
		p=1 
		print"Eyes closed"
		GPIO.output(buzz,GPIO.HIGH)	#eyesclosed
	
	
   
	if((axes['x'] < 0 and axes['y'] < 0) and (p==1) ):            #right side
		GPIO.output(buzz,GPIO.LOW)
		print"stop"
		#GPIO.output(motor,GPIO.LOW)
		#GPIO.cleanup()
                print "Stopping Motor"
		break

			
	elif((axes['x']>0.95) and (p==1)):				#left side
		GPIO.output(buzz,GPIO.LOW)
		print"stop"
	        #GPIO.output(motor,GPIO.LOW)
                #GPIO.cleanup()
	        print "Stopping Motor"
		break
			
	elif((axes['y']<0 and axes['x']<0.4) and (p==1)):                            #front side
	   	print"stop"
	   	GPIO.output(buzz,GPIO.LOW)
	   	#GPIO.output(motor,GPIO.LOW)
                #GPIO.cleanup()
	   	print "Stopping Motor"
	        break
	accel_xout= accel_xout1
   	accel_yout= accel_yout1
   	accel_zout= accel_zout1
	time.sleep(1)				
	
time.sleep(2)
cras()
	

	
	
		