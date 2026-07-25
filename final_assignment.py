from yolo_uno import *
from pins import *
from lcd1602 import *
from dht20 import *
import asyncio

class Semaphore:
    def __init__(self, value=1):
        if value < 0:
            raise ValueError("ValueError")
        self.value = value
        self.waiting = []

    async def acquire(self):
        if self.value > 0:
            self.value -= 1
            return True
        
        curr_task = asyncio.current_task() if hasattr(asyncio, 'current_task') else None
        self.waiting.append(curr_task)
        
        ev = asyncio.Event()
        async def wait_placeholder():
            await ev.wait()
            
        while self.value <= 0:
            await asleep_ms(10)
            if curr_task not in self.waiting: 
                break
                
        self.value -= 1
        return True

    def release(self):
        self.value += 1
        if self.waiting:
            task = self.waiting.pop(0)

TEMP_SAFE_MIN = 22.0
TEMP_SAFE_MAX = 26.0
TEMP_RISKY_MIN = 27.0
TEMP_DANGER = 30.0
HUMID_LOW_THRESH = 40.0

current_temp = 0.0
current_humid = 0.0

heater_sem = Semaphore(0)
cooler_sem = Semaphore(0)
humid_sem = Semaphore(0)

led_D13 = Pins(D13_PIN)
rgb_led_D3 = RGBLed(D3_PIN, 4)
rgb_led_D5 = RGBLed(D5_PIN, 4)
rgb_led_D7 = RGBLed(D7_PIN, 4)
lcd1602 = LCD1602()
dht20 = DHT20()


async def task_LED_Blinky():
    while True:
        await asleep_ms(1000)
        led_D13.toggle()

async def task_Heater():
    global current_temp
    while True:
        await heater_sem.acquire()
        
        if TEMP_SAFE_MIN <= current_temp <= TEMP_SAFE_MAX:
            rgb_led_D3.show(0, hex_to_rgb('#00ff00'))
        elif TEMP_RISKY_MIN <= current_temp < TEMP_DANGER:
            rgb_led_D3.show(0, hex_to_rgb('#ffa500'))
        else:
            rgb_led_D3.show(0, hex_to_rgb('#ff0000'))

async def task_Cooler():
    global current_temp
    while True:
        await cooler_sem.acquire()
        print("Cooler Activated!")
        rgb_led_D5.show(0, hex_to_rgb('#00ff00'))
        
        await asleep_ms(5000)
        
        rgb_led_D5.show(0, hex_to_rgb('#000000'))

async def task_Humidifier():
    global current_humid
    while True:
        await humid_sem.acquire()
        print("Humidifier State Machine Started")
        
        rgb_led_D7.show(0, hex_to_rgb('#00ff00'))
        await asleep_ms(5000)
        
        rgb_led_D7.show(0, hex_to_rgb('#ffff00'))
        await asleep_ms(3000)
        
        rgb_led_D7.show(0, hex_to_rgb('#ff0000'))
        await asleep_ms(2000)
        
        rgb_led_D7.show(0, hex_to_rgb('#000000'))

async def task_ReadSensor():
    global current_temp, current_humid
    while True:
        current_temp = await dht20.atemperature()
        current_humid = await dht20.ahumidity()
        
        print("Temp:", current_temp, "C | Humid:", current_humid, "%")
        lcd1602.clear()
        lcd1602.show("Temp: " + str(current_temp) + " C", 0, 0)
        lcd1602.show("Humid: " + str(current_humid) + " %", 1, 0)
        
        heater_sem.release()
        
        if current_temp >= TEMP_DANGER:
            cooler_sem.release()
            
        if current_humid < HUMID_LOW_THRESH:
            humid_sem.release()
            
        await asleep_ms(5000)

async def setup():
    print('Smart Climate System Started')
    create_task(task_LED_Blinky())
    create_task(task_ReadSensor())
    create_task(task_Heater())
    create_task(task_Cooler())
    create_task(task_Humidifier())

async def main():
    await setup()
    while True:
        await asleep_ms(100)

run_loop(main())