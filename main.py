from machine import Pin, time_pulse_us
from utime import sleep_us, sleep_ms

l1=Pin(12,Pin.OUT)
l2=Pin(13,Pin.OUT)
trip=Pin(16,Pin.OUT)
echp=Pin(17,Pin.IN)
buz=Pin(15,Pin.OUT)

SOUND_SPEED=340
dis_ob=[200,0]

while True:
    l1.off()
    l2.on()
    buz.on()
    trip.value(0)
    sleep_us(5)

    trip.value(1)
    sleep_us(10)
    trip.value(0)

    ultrason_duration = time_pulse_us(echp, 1, 30000) 
    distance_cm = SOUND_SPEED * ultrason_duration / 20000
    dis_ob.append(distance_cm)

    print(f"Distance : {distance_cm} cm")
    print("x1 = ",dis_ob[-1])
    print("x2 = ", dis_ob[-2])
    x1=dis_ob[-1]
    x2=dis_ob[-2]
    xr=x2-x1
    print("xr = ",xr)
    if xr>=10:
        print("alter")
        l2.off()
        l1.on()
        buz.off()
        sleep_ms(500)
    sleep_ms(200)