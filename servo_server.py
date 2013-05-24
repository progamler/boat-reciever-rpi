#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time
import socket
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x40, debug=True)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
servo = 300
pwm.setPWM(0, 0, 500)
time.sleep(2)



HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr
while (True):
  data = conn.recv(1024)
  if not data: break
  conn.sendall(data)
  print(data)
  if data.startswith("+"):
    if servo < servoMax:
      servo = servo+5
  elif data == "quit":
    print("quit\n")
  else:
    if servo > servoMin:
      servo = servo-5
  print(servo)
  pwm.setPWM(0, 0, servo)
  # Change speed of continuous servo on channel O
  #pwm.setPWM(0, 0, servoMin)
  #time.sleep(1)
  #pwm.setPWM(0, 0, servoMax)
  #time.sleep(1)



