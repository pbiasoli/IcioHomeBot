#IcioHomeBot v0.2

#Connection:
#L_black: ground
#L_green: GPIO11
#T_black: ground
#T_red: 3V
#T_yellow: GPIO7

# To start at raspberry boot, put in /etc/rc.local the line: su - pi -c "screen -dm -S iciobot python /home/pi/iciobot/IcioHomeBot.py"

import sys
import time
import random
import datetime
import telepot
import json
import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor

# Variables from json
with open("IcioHomeBotVar.json") as json_file:
  IcioHomeBotVar = json.load(json_file)
	token = IcioHomeBotVar['token']
	latitude = IcioHomeBotVar['latitude']
  longitude = IcioHomeBotVar['longitude']
  W1ThermSensorID1 = IcioHomeBotVar['W1ThermSensorID1']

#LED
def on(pin):
  GPIO.output(pin,GPIO.HIGH)
  return
def off(pin):
  GPIO.output(pin,GPIO.LOW)
  return
def click(pin):
  GPIO.output(pin,GPIO.HIGH)
  time.sleep(.5)
  GPIO.output(pin,GPIO.LOW)
  return

GPIO_ID = 11
# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
# set up GPIO output channel
GPIO.setup(GPIO_ID, GPIO.OUT)
# starting off
off(GPIO_ID)

#DS18B20 with ID W1ThermSensorID1
sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, W1ThermSensorID1)

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text'].lower()

    print ('Got command: ' + command)

    if command == 'on':
        on(GPIO_ID)
        bot.sendMessage(chat_id, 'Led On')
    elif command =='off':
        off(GPIO_ID)
        bot.sendMessage(chat_id, 'Led Off')
    elif command =='click':
        click(GPIO_ID)
        bot.sendMessage(chat_id, 'Click')
    elif command =='blink':
        bot.sendMessage(chat_id, 'Blink Start')
        for i in range(5):
            on(GPIO_ID)
            time.sleep(.5)
            off(GPIO_ID)
            time.sleep(.5)
        bot.sendMessage(chat_id, 'Blink End')
    elif command =='temp':
        temperature_in_celsius = sensor.get_temperature()
        bot.sendMessage(chat_id, 'Temperature is: ' + str(temperature_in_celsius))
    else:
        bot.sendMessage(chat_id, 'I do not understand... :(')

temperature_in_celsius = sensor.get_temperature()

bot = telepot.Bot(token)
bot.message_loop(handle)
print ('I am listening...')

while 1:
     time.sleep(10)
