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
import urequests
machine.freq(80000000)
esp.osdebug(None)
touch=machine.TouchPad(machine.Pin(33))
touch.config(1000)
esp32.wake_on_touch(True)
print(os.uname())
def time_get():
    ntptime.settime()
def wlan():
    global sta_if
    sta_if=network.WLAN(network.STA_IF)
    sta_if.active(True)
    #sta_if.connect('a-itswireless','1234567890')
    sta_if.connect('Christopher_M_Johnston','OdinRoot')
try:
    if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        print("Woke From Deepsleep")
        pass
    else:
        wlan()
        while True:
                if sta_if.isconnected()==True:
                    mac=ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
                    ip=sta_if.ifconfig()
                    print(ip)
                    try:
                        time_get()
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
                    ip=sta_if.ifconfig()
                    print(ip)
                    print(mac)
                    gled.value(1)
                    bled.value(0)
                    ds.convert_temp()
                    time.sleep_ms(750)
                    gled.value(0)
                    print(rtc.datetime())
                    for rom in roms:
                        temperature=((float((ds.read_temp(rom))*(1.8))+32)-2)
                        print(temperature)
                    push = urequests.get("http://10.132.93.117:5050/226ABF03-139B-41EA-BA2D-882AA66C8D0E?value=%f"%(temperature))
                    break
                except:
                    pass
            else:
                time.sleep_ms(10)
                pass
    rled.value(1)
    time.sleep_ms(30)
    temp_power.value(0)
    machine.deepsleep(900000)
except:
    machine.deepsleep(900000)