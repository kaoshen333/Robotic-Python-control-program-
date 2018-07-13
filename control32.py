import RPi.GPIO as GPIO
import time
from TRSensors import TRSensor

from AlphaBot2 import AlphaBot2

Button = 7

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(Button,GPIO.IN,GPIO.PUD_UP)

class AlphaBot2(object):

	def __init__(self,ain1=12,ain2=13,ena=6,bin1=20,bin2=21,enb=26):
		self.AIN1 = ain1
		self.AIN2 = ain2
		self.BIN1 = bin1
		self.BIN2 = bin2
		self.ENA = ena
		self.ENB = enb
		self.PA  = 50
		self.PB  = 50

		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.AIN1,GPIO.OUT)
		GPIO.setup(self.AIN2,GPIO.OUT)
		GPIO.setup(self.BIN1,GPIO.OUT)
		GPIO.setup(self.BIN2,GPIO.OUT)
		GPIO.setup(self.ENA,GPIO.OUT)
		GPIO.setup(self.ENB,GPIO.OUT)
		self.PWMA = GPIO.PWM(self.ENA,500)
		self.PWMB = GPIO.PWM(self.ENB,500)
		self.PWMA.start(self.PA)
		self.PWMB.start(self.PB)
		self.stop()

	def forward(self):
		self.PWMA.ChangeDutyCycle(self.PA)
		self.PWMB.ChangeDutyCycle(self.PB)
		GPIO.output(self.AIN1,GPIO.LOW)
		GPIO.output(self.AIN2,GPIO.HIGH)
		GPIO.output(self.BIN1,GPIO.LOW)
		GPIO.output(self.BIN2,GPIO.HIGH)


	def stop(self):
		self.PWMA.ChangeDutyCycle(0)
		self.PWMB.ChangeDutyCycle(0)
		GPIO.output(self.AIN1,GPIO.LOW)
		GPIO.output(self.AIN2,GPIO.LOW)
		GPIO.output(self.BIN1,GPIO.LOW)
		GPIO.output(self.BIN2,GPIO.LOW)

	def backward(self):
		self.PWMA.ChangeDutyCycle(self.PA)
		self.PWMB.ChangeDutyCycle(self.PB)
		GPIO.output(self.AIN1,GPIO.HIGH)
		GPIO.output(self.AIN2,GPIO.LOW)
		GPIO.output(self.BIN1,GPIO.HIGH)
		GPIO.output(self.BIN2,GPIO.LOW)

		
	def left(self):
		self.PWMA.ChangeDutyCycle(30)
		self.PWMB.ChangeDutyCycle(30)
		GPIO.output(self.AIN1,GPIO.HIGH)
		GPIO.output(self.AIN2,GPIO.LOW)
		GPIO.output(self.BIN1,GPIO.LOW)
		GPIO.output(self.BIN2,GPIO.HIGH)


	def right(self):
		self.PWMA.ChangeDutyCycle(30)
		self.PWMB.ChangeDutyCycle(30)
		GPIO.output(self.AIN1,GPIO.LOW)
		GPIO.output(self.AIN2,GPIO.HIGH)
		GPIO.output(self.BIN1,GPIO.HIGH)
		GPIO.output(self.BIN2,GPIO.LOW)
		
	def setPWMA(self,value):
		self.PA = value
		self.PWMA.ChangeDutyCycle(self.PA)

	def setPWMB(self,value):
		self.PB = value
		self.PWMB.ChangeDutyCycle(self.PB)	
		
	def setMotor(self, left, right):
		if((right >= 0) and (right <= 100)):
			GPIO.output(self.AIN1,GPIO.HIGH)
			GPIO.output(self.AIN2,GPIO.LOW)
			self.PWMA.ChangeDutyCycle(right)
		elif((right < 0) and (right >= -100)):
			GPIO.output(self.AIN1,GPIO.LOW)
			GPIO.output(self.AIN2,GPIO.HIGH)
			self.PWMA.ChangeDutyCycle(0 - right)
		if((left >= 0) and (left <= 100)):
			GPIO.output(self.BIN1,GPIO.HIGH)
			GPIO.output(self.BIN2,GPIO.LOW)
			self.PWMB.ChangeDutyCycle(left)
		elif((left < 0) and (left >= -100)):
			GPIO.output(self.BIN1,GPIO.LOW)
			GPIO.output(self.BIN2,GPIO.HIGH)
			self.PWMB.ChangeDutyCycle(0 - left)


if __name__=='__main__':

	Ab = AlphaBot2()
	TR = TRSensor()
	Ab.stop()
	print("Line follow Example")
	time.sleep(0.5)
	for i in range(0,100):
		if(i<25 or i>= 75):
			Ab.right()
			Ab.setPWMA(20)
			Ab.setPWMB(20)
		else:
			Ab.left()
			Ab.setPWMA(20)
			Ab.setPWMB(20)
		TR.calibrate()
	Ab.stop()
	print(TR.calibratedMin)
	print(TR.calibratedMax)
	while (GPIO.input(Button) != 0):
		position,Sensors = TR.readLine()
		print(position,Sensors)
		time.sleep(0.05)
	#Ab.forward()
	#Ab.forward()  #333
	try:
		while True:
			#time.sleep(0.005)   #333 add 
			position,Sensors = TR.readLine()
			#print('position is %5.3f.' % position)   #Allen add
	#print(position)   #Allen need
			print('Sensors0 is %5.3f.' % Sensors[0])
			print('Sensors1 is %5.3f.' % Sensors[1])
			print('Sensors2 is %5.3f.' % Sensors[2])
			print('Sensors3 is %5.3f.' % Sensors[3])
			print('Sensors4 is %5.3f.' % Sensors[4])
		
			if(Sensors[0]<100 and Sensors[1]<100 and Sensors[2]<100 and Sensors[3]<100 and Sensors[4]<100):
				#Ab.setPWMA(0)
				#Ab.setPWMB(0);
				Ab.stop()
			elif(Sensors[0]>600 and Sensors[1]>600 and Sensors[2]>600 and Sensors[3]>600 and Sensors[4]>600):
				Ab.setPWMA(30)            #comment these two
				Ab.setPWMB(30)
				#for num in range(0,10):
				Ab.left()
				
				time.sleep(0.002)           # this comes from avidance demo 
				Ab.stop()
				
				'''
				Ab.left()
				Ab.left()
				Ab.left()
				Ab.left()
				Ab.left()
				Ab.left()
				Ab.left()
				Ab.left();
				'''

			elif((Sensors[0]<100 and Sensors[1] >600 and Sensors[2] >600) or( Sensors[2] >600 and Sensors[3] >600 and Sensors[4]<100)):
				Ab.forward()
			elif(Sensors[0] >600 and Sensors[4]<100 ):
				Ab.left()
				#time.sleep(0.005);
			elif(Sensors[0]<100 and Sensors[4] >600 ):
				Ab.right()
				#time.sleep(0.005);
			else:
				Ab.forward()
			#time.sleep(1)
				#time.sleep(0.005)
				
				
	except KeyboardInterrupt:
		GPIO.cleanup()
