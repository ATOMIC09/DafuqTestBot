from time import sleep
import serial

ser = serial.Serial('com5',9600)
sleep(2)

def dht11_out():
	try :
		data =[]						# empty list to store the data
		for i in range(1):
			b = ser.readline()			# read a byte string
			string_n = b.decode()		# decode byte string into Unicode  
			string = string_n.rstrip()	# remove \n and \r
			data.append(string)			# add to the end of data list
			sleep(0.1)					# wait (sleep) 0.1 seconds
		ser.close()
		return string
	except :
		return "ไม่พบการเชื่อมต่อของเซ็นเซอร์ โปรดตรวจสอบเซ็นเซอร์และรีบูตบอท"
		