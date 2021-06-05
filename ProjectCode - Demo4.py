import sys
import os
import time
import datetime
import RPi.GPIO as GPIO
import MySQLdb

# Setting up the LDRs.
global c
global db

GPIO.setmode(GPIO.BOARD)

resistorPin1 = 7
resistorPin2 = 11
resistorPin3 = 13
resistorPin4 = 15

# Setting up the motors.
input1 = 29
input2 = 31
input3 = 37
input4 = 35
en2 = 33
en1 = 32

GPIO.setup(input1, GPIO.OUT)
GPIO.setup(input2, GPIO.OUT)
GPIO.setup(input3, GPIO.OUT)
GPIO.setup(input4, GPIO.OUT)
GPIO.setup(en1,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)

GPIO.output(input1,GPIO.LOW)
GPIO.output(input2,GPIO.LOW)
GPIO.output(input3,GPIO.LOW)
GPIO.output(input4,GPIO.LOW)

#Controlling the motors using Pulse Width Modulation.
p1 = GPIO.PWM(en1,500)
p2 = GPIO.PWM(en2,500)
p1.start(50)
p2.start(50)

def getLDRreadings(resistorPin):
    GPIO.setup(resistorPin, GPIO.OUT)
    GPIO.output(resistorPin, GPIO.LOW)
    time.sleep(0.1)
    
    GPIO.setup(resistorPin, GPIO.IN)
    currentTime = time.time()
    ldr = 0
    
    while(GPIO.input(resistorPin) == GPIO.LOW):
        ldr = time.time() - currentTime
    
    return (ldr*1000)

def forward(inputA,inputB):
    
    GPIO.output(inputA, GPIO.LOW)
    GPIO.output(inputB, GPIO.HIGH)
    print("Moving Forward")
    
def reverse(inputA,inputB):
    GPIO.output(inputA, GPIO.HIGH)
    GPIO.output(inputB, GPIO.LOW)
    print("Moving Backward")
    
def stop(inputA,inputB):
    GPIO.output(inputA, GPIO.LOW)
    GPIO.output(inputB, GPIO.LOW)
    print("Stopping")

def insert_to_db():
    ldr1 = getLDRreadings(resistorPin1)
    ldr2 = getLDRreadings(resistorPin2)
    ldr3 = getLDRreadings(resistorPin3)
    ldr4 = getLDRreadings(resistorPin4)
    t = (datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")) #Time of the LDR reading.
    d = (datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d")) #Date of the LDR reading.
    
    sql =  "INSERT INTO capacitor_charge_time (Date, Time, LDR1, LDR2, LDR3, LDR4) VALUES (%s, %s, %s, %s, %s, %s)" 
    try:
        c.execute(sql,( str(d) , str(t), str(ldr1), str(ldr2), str(ldr3), str(ldr4)))
        db.commit()
    except:
        db.rollback()
                  
def main():
    while 1:
        insert_to_db()
        time.sleep(0.1)
        
        ldr1 = getLDRreadings(resistorPin1)
        ldr2 = getLDRreadings(resistorPin2)
        ldr3 = getLDRreadings(resistorPin3)
        ldr4 = getLDRreadings(resistorPin4)
        
        if (ldr1+ldr2) > 1.1*(ldr3+ldr4):
            forward(input3,input4)
        elif (ldr1+ldr2) < 0.9*(ldr3+ldr4):
            reverse(input3,input4)
        else:
            stop(input3,input4)
            
        time.sleep(0.1)
            
        if (ldr1+ldr3) > 1.1*(ldr2+ldr4):
            forward(input1,input2)
        elif (ldr1+ldr3) < 0.9*(ldr2+ldr4):
            reverse(input1,input2)
        else:
            stop(input1,input2)
            
        time.sleep(0.1)
        
if __name__ == '__main__':
    try:
        db = MySQLdb.connect("localhost","yossof","1234","LDS")
        c= db.cursor()
    except:
        print ("Can't Connect to Database...")         
    try:
      main()
          
    except KeyboardInterrupt:
      print ("Bye Bye...")
      GPIO.cleanup()
      pass        