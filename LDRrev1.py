import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

resistorPin = 7

while True:
    GPIO.setup(resistorPin, GPIO.OUT)
    GPIO.output(resistorPin, GPIO.LOW)
    time.sleep(0.1)
    
    GPIO.setup(resistorPin, GPIO.IN)
    currentTime = time.time()
    ldr1 = 0
    
    while(GPIO.input(resistorPin) == GPIO.LOW):
        ldr1 = time.time() - currentTime
        
    print (ldr1*1000)
    time.sleep(1)
    