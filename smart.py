import RPi.GPIO as GPIO
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
try:
    GPIO.setmode(GPIO.BOARD)
    
    PIN_TRIGGER = 7
    PIN_ECHO = 11
    
    GPIO.setup(PIN_TRIGGER,GPIO.OUT)
    GPIO.setup(PIN_ECHO,GPIO.IN)
    
    GPIO.output(PIN_TRIGGER,GPIO.LOW)
    
    print("Waiting for sensor to settle")
    
    time.sleep(2)
    
    print("Calculating distance")
    
    GPIO.output(PIN_TRIGGER,GPIO.HIGH)
    
    time.sleep(0.00001)
    
    GPIO.output(PIN_TRIGGER,GPIO.LOW)
    
    while GPIO.input(PIN_ECHO)==0 :
        pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO)==1 :
        pulse_end_time = time.time()
        
    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)
    print("Distance :",distance,"cm")
    
    if distance>5:
        fromaddr = "rait1033@gmail.com"
        toaddr = "siddhesh.esskay.92@gmail.com"
        msg = MIMEMultipart()
        
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Raspberry Pi"
        
        body = "Dustbin is 75% full"
        msg.attach(MIMEText(body,'plain'))
                            
        server = smtplib.SMTP('smtp.gmail.com', port=587)
        server.starttls()
        server.login(fromaddr, 'Raspberrypi')
        
        text = msg.as_string()
        server.sendmail(fromaddr,toaddr,text)
        server.quit()
        print('message sent')
    
    
        
finally:
    GPIO.cleanup()
