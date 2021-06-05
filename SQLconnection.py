import os
import time
import datetime
import MySQLdb
import RPi.GPIO as GPIO

global c
global db

GPIO.setmode(GPIO.BOARD)

resistorPin1 = 7

def getLDR1readings():
    GPIO.setup(resistorPin1, GPIO.OUT)
    GPIO.output(resistorPin1, GPIO.LOW)
    time.sleep(0.1)
    
    GPIO.setup(resistorPin1, GPIO.IN)
    currentTime = time.time()
    ldr1 = 0
    
    while(GPIO.input(resistorPin1) == GPIO.LOW):
        ldr1 = time.time() - currentTime
    return (ldr1)

def insert_to_db():
    ldr1 = (getLDR1readings()*1000)
    t = (datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S"))
    d = (datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d"))
    print (str(ldr1) + " - " + t + " - " + d)
    sql =  "INSERT INTO capacitor_charge_time (Date, Time, LDR1) VALUES (%s, %s, %s)" 
    try:
        c.execute(sql,( str(d) , str(t), str(ldr1)))
        db.commit()
    except:
        db.rollback()

def read_from_db():
    try:
        c.execute("SELECT * FROM capacitor_charge_time ORDER BY ID DESC LIMIT 1")      
        result = c.fetchall()
        if result is not None:
             print ('Date ' , result[0][1], '| Time: ' , result[0][2], ' | Capacitor Charge Time: ' , result[0][3], 'milliseconds')
    except:
        print ("Reading Error")
    
def main():
    while 1:
        insert_to_db()
        read_from_db()
        time.sleep(1)
    
        
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
      pass
  