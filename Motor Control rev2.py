import sys
import time
import RPi.GPIO as GPIO

input1 = 29
input2 = 31
input3 = 37
input4 = 35
en2 = 33
en1 = 32

GPIO.setmode(GPIO.BOARD)
GPIO.setup(input1, GPIO.OUT)
GPIO.setup(input2, GPIO.OUT)
GPIO.setup(en1,GPIO.OUT)

GPIO.output(input1,GPIO.LOW)
GPIO.output(input2,GPIO.LOW)

p=GPIO.PWM(en1,500)
p.start(50)

def forward():
    
    GPIO.output(input1, GPIO.LOW)
    GPIO.output(input2, GPIO.HIGH)
    print("Moving Forward")
    
def reverse():
    GPIO.output(input1, GPIO.HIGH)
    GPIO.output(input2, GPIO.LOW)
    print("Moving Backward")
    
def main():
    while 1:
        reverse()
        time.sleep(10)
        GPIO.cleanup()
    
if __name__ == '__main__':     
    try:
      main()
    except KeyboardInterrupt:
      print ("Bye Bye...")
      GPIO.cleanup()
      pass
  