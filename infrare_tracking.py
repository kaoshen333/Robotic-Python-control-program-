# infrare tracking using 2-5 infrare sensor using digit 0 and 1 
#IO.setup(14,IO.IN) #GPIO 14 -> IR sensor as input          #right infrare sensor

import RPi.GPIO as GPIO
import time
from AlphaBot2 import AlphaBot2

Ab = AlphaBot2()

DR =             #right infrare sensor    # gpio readall  command 
DL =             #left infrare sensor

TrackPin =       #right infrare sensor
LedPin   = 



def setup():
	#GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	#GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
	#GPIO.setup(TrackPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	#GPIO.output(LedPin, GPIO.HIGH) # Set LedPin high(+3.3V) to off led
	
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
	GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

	GPIO.setup(TrackPin,GPIO.IN,GPIO.PUD_UP)
	GPIO.setup(LedPin,GPIO.OUT)
	GPIO.output(LedPin, GPIO.HIGH) # Set LedPin high(+3.3V) to off led

def loop():
	while True:
		if GPIO.input(TrackPin) == GPIO.LOW:
			print 'White line is detected'
			GPIO.output(LedPin, GPIO.LOW)  # led on
			
			Ab.left()
		#Ab.right()
			time.sleep(0.002)
			Ab.stop()
		
		else:
			print '...Black line is detected'
			GPIO.output(LedPin, GPIO.HIGH) # led off
			
			Ab.forward()

def destroy():
	GPIO.output(LedPin, GPIO.HIGH)     # led off
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

'''		
while True:
	DR_status = GPIO.input(DR)
	DL_status = GPIO.input(DL)
		print(DR_status,DL_status)     # test 0 1 output of infrare
	if((DL_status == 0) or (DR_status == 0)):
		Ab.left()
		#Ab.right()
		time.sleep(0.002)
		Ab.stop()
	#	print("object")
	else:
		Ab.forward()
	#	print("forward")