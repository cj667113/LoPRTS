import machine
import os
import time
import onewire
import ds18x20
import network
import esp
import esp32
import ubinascii
import ntptime
import usgota
from umqtt_simple import MQTTClient
mqtt_server = 'host'
machine.freq(80000000)
esp.osdebug(None)
touch=machine.TouchPad(machine.Pin(33))
touch.config(1000)
esp32.wake_on_touch(True)
adc_pin = machine.Pin(35)
adc=machine.ADC(adc_pin)
adc.atten(adc.ATTN_11DB)
print(os.uname())
client_id = ubinascii.hexlify(machine.unique_id())
timer=machine.Timer(-1)
timer.init(period=120000, mode=machine.Timer.PERIODIC, callback=lambda t:machine.deepsleep(900000))
def time_get():
    ntptime.settime()
def voltage_read():
    global vval
    vval=adc.read()
    vval=vval*(3.3/4095)
    print(vval)
def wlan():
    voltage_read()
    global sta_if
    sta_if=network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('','')
def connect_and_subscribe(topic,data):
    c = MQTTClient(client_id, mqtt_server,user='',password='')
    c.connect()
    c.publish(topic, data)
    c.disconnect()
try:
    if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        print("Woke From Deepsleep")
        pass
    elif machine.reset_cause()==machine.WDT_RESET:
        print("Watch Dog Time Expired")
        pass
    else:
        wlan()
        while True:
                if sta_if.isconnected()==True:
                    mac=ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
                    mac=mac.replace(':','-')
                    ip=sta_if.ifconfig()
                    print(ip)
                    try:
                        time_get()
                        time.sleep_ms(10)
                        usgota.update("https://api.github.com/repos/cj667113/LoPRTS/commits?path=LoPRTS_Code/Temperature_mqtt.py")
                        time.sleep_ms(10)
                        print("Going to Deepsleep")
                        break
                    except:
                        pass
                else:
                    time.sleep_ms(10)
                    pass 
        machine.deepsleep()
    rtc=machine.RTC()
    temp_power = machine.Pin(32,machine.Pin.OUT)
    temp_power.value(1)
    rled=machine.Pin(18,machine.Pin.OUT)
    bled=machine.Pin(5,machine.Pin.OUT)
    bled.value(1)
    gled=machine.Pin(17,machine.Pin.OUT)
    temp_data = machine.Pin(12)
    ds = ds18x20.DS18X20(onewire.OneWire(temp_data))
    roms = ds.scan()
    print(roms)
    temperature = 0
    wlan()
    while True:
            if sta_if.isconnected()==True:
                try:
                    mac=ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
                    mac=mac.replace(':','-')
                    ip=sta_if.ifconfig()
                    print(ip)
                    usgota.update("https://api.github.com/repos/cj667113/LoPRTS/commits?path=LoPRTS_Code/Temperature_mqtt.py")
                    timer=machine.Timer(-1)
                    timer.init(period=15000, mode=machine.Timer.PERIODIC, callback=lambda t:machine.deepsleep(900000))
                    gled.value(1)
                    bled.value(0)
                    ds.convert_temp()
                    time.sleep_ms(750)
                    gled.value(0)
                    print(rtc.datetime())
                    for rom in roms:
                        temperature=((float((ds.read_temp(rom))*(1.8))+32)-2)
                    voltage_read()
                    topic=(mac+'/Temperature')
                    topic.encode()
                    print(topic)
                    temperature=str(temperature)
                    connect_and_subscribe(topic,temperature)
                    vval=str(vval)
                    topic=(mac+'/Voltage')
                    topic.encode()
                    connect_and_subscribe(topic,vval)
                    print(topic)
                    print(temperature)
                    time.sleep_ms(10)
                    break
                except:
                    raise
            else:
                time.sleep_ms(10)
                pass
    rled.value(1)
    time.sleep_ms(30)
    temp_power.value(0)
    machine.deepsleep(900000)
except:
    machine.deepsleep(900000)
