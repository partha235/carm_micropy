# program with web control button for car with AP mode. 

try:
    import usocket as socket    # socket module allow us to send response over network.
except:
    import socket
from utime import sleep_ms, sleep
import network 
from machine import Pin
import gc 

try:
    from bps_cre import *     
except:
    pass

gc.collect()

# led=Pin("LED",Pin.OUT) # for Raspberry Pi Pico
led = Pin(2, Pin.OUT)   # for esp boards
# pins for car motor
ma1 = Pin(4, Pin.OUT)
ma2 = Pin(16, Pin.OUT)
mb1 = Pin(17, Pin.OUT)
mb2 = Pin(5, Pin.OUT)


ssid = 'bps_explore'
password = '123456789'  # your network/hotspot/ssid password.

""" in this program I used network with station mode, which mean the board connect
to the network which we programed to connect """
ap = network.WLAN(network.AP_IF)
ap.active(True)

ap.ifconfig(('192.168.4.23', '255.255.255.0', '192.168.4.23', '8.8.8.8'))

ap.config(essid=ssid, password=password)

# connecting to network.
# sleep(1)
print("connection status : ", ap.isconnected())

while ap.isconnected()==False:
    pass

if ap.isconnected():
    print("connection status : ", ap.isconnected())
    
# (IP,Subnet,Gateway,DNS) here i declared that i need my own ip address; where leaving it 
# make auto ip address according to our network.
print(ap.ifconfig())

def web_page():
    html = """
            <!DOCTYPE html>
        <html lang="en">
        
        <head>
            <meta charset="UTF-8">
        
            <meta name="viewport"
                  content="width=device-width, initial-scale=1.0">
        
            <title>Robotic Vehicle Control</title>
        
            <style>
        
                * {
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }
        
                body {
                    min-height: 100vh;
                    background: #111827;
                    color: #e5e7eb;
        
                    font-family:
                        Arial,
                        Helvetica,
                        sans-serif;
        
                    display: flex;
                    justify-content: center;
                    align-items: center;
        
                    padding: 20px;
                }
        
                /* =========================
                   MAIN CONTROL PANEL
                   ========================= */
        
                .control-panel {
                    width: 100%;
                    max-width: 520px;
        
                    background: #1f2937;
        
                    border: 1px solid #374151;
        
                    border-radius: 16px;
        
                    padding: 30px;
        
                    box-shadow:
                        0 20px 50px rgba(0, 0, 0, 0.35);
                }
        
                /* =========================
                   HEADER
                   ========================= */
        
                .header {
                    text-align: center;
                    margin-bottom: 25px;
                }
        
                .header h1 {
                    font-size: 26px;
                    font-weight: 600;
                    color: #f9fafb;
        
                    margin-bottom: 8px;
                }
        
                .header p {
                    font-size: 14px;
                    color: #9ca3af;
                }
        
                /* =========================
                   STATUS
                   ========================= */
        
                .status {
                    display: flex;
                    justify-content: center;
                    align-items: center;
        
                    gap: 8px;
        
                    margin-bottom: 25px;
        
                    font-size: 14px;
                    color: #d1d5db;
                }
        
                .status-dot {
                    width: 10px;
                    height: 10px;
        
                    background: #22c55e;
        
                    border-radius: 50%;
        
                    box-shadow:
                        0 0 10px rgba(34, 197, 94, 0.7);
                }
        
                /* =========================
                   CONTROL AREA
                   ========================= */
        
                .controls {
                    display: flex;
                    flex-direction: column;
        
                    align-items: center;
        
                    gap: 12px;
                }
        
                .control-row {
                    display: flex;
                    justify-content: center;
        
                    gap: 12px;
                }
        
                /* =========================
                   CONTROL BUTTON
                   ========================= */
        
                .control-button {
        
                    width: 90px;
                    height: 70px;
        
                    border: 1px solid #4b5563;
        
                    border-radius: 12px;
        
                    background: #374151;
        
                    color: #f9fafb;
        
                    font-size: 30px;
        
                    cursor: pointer;
        
                    transition:
                        background 0.15s,
                        transform 0.1s,
                        border-color 0.15s;
        
                    user-select: none;
        
                    -webkit-user-select: none;
        
                    touch-action: manipulation;
                }
        
                .control-button:hover {
        
                    background: #4b5563;
        
                    border-color: #6b7280;
                }
        
                .control-button:active {
        
                    transform: scale(0.94);
        
                    background: #2563eb;
        
                    border-color: #60a5fa;
                }
        
                /* =========================
                   STOP BUTTON
                   ========================= */
        
                .stop-button {
        
                    width: 194px;
                    height: 60px;
        
                    margin-top: 10px;
        
                    border: none;
        
                    border-radius: 12px;
        
                    background: #dc2626;
        
                    color: white;
        
                    font-size: 17px;
        
                    font-weight: 600;
        
                    cursor: pointer;
        
                    transition:
                        background 0.15s,
                        transform 0.1s;
                }
        
                .stop-button:hover {
        
                    background: #ef4444;
                }
        
                .stop-button:active {
        
                    transform: scale(0.96);
        
                    background: #b91c1c;
                }
        
                /* =========================
                   LABELS
                   ========================= */
        
                .button-label {
        
                    display: block;
        
                    font-size: 11px;
        
                    color: #9ca3af;
        
                    margin-top: 5px;
        
                    text-transform: uppercase;
        
                    letter-spacing: 0.8px;
                }
        
                /* =========================
                   FOOTER
                   ========================= */
        
                .footer {
        
                    text-align: center;
        
                    margin-top: 25px;
        
                    padding-top: 18px;
        
                    border-top: 1px solid #374151;
        
                    font-size: 12px;
        
                    color: #6b7280;
                }
        
                /* =========================
                   MOBILE
                   ========================= */
        
                @media (max-width: 480px) {
        
                    .control-panel {
        
                        padding: 22px;
        
                    }
        
                    .control-button {
        
                        width: 78px;
                        height: 65px;
        
                        font-size: 26px;
        
                    }
        
                    .stop-button {
        
                        width: 168px;
        
                    }
        
                }
        
            </style>
        
            <script>
        
                /*
                 * ==============================
                 * SEND COMMAND TO ROBOT
                 * ==============================
                 */
        
                function sendRequest(command) {
        
                    var xhr = new XMLHttpRequest();
        
                    xhr.open(
                        "GET",
                        "/?action=" + encodeURIComponent(command),
                        true
                    );
        
                    xhr.send();
        
                }
        
        
                /*
                 * ==============================
                 * START MOVEMENT
                 * ==============================
                 */
        
                function startMovement(command) {
        
                    sendRequest(command);
        
                }
        
        
                /*
                 * ==============================
                 * STOP MOVEMENT
                 * ==============================
                 */
        
                function stopMovement() {
        
                    sendRequest("stop");
        
                }
        
        
                /*
                 * ==============================
                 * PREVENT CONTEXT MENU
                 * ==============================
                 */
        
                document.addEventListener(
                    "contextmenu",
                    function(event) {
        
                        event.preventDefault();
        
                    }
                );
        
            </script>
        
        </head>
        
        
        <body>
        
            <main class="control-panel">
        
        
                <!-- =========================
                     HEADER
                     ========================= -->
        
                <header class="header">
        
                    <h1>
                        Robotic Vehicle Control
                    </h1>
        
                    <p>
                        Remote Navigation Interface
                    </p>
        
                </header>
        
        
                <!-- =========================
                     STATUS
                     ========================= -->
        
                <div class="status">
        
                    <span class="status-dot"></span>
        
                    <span>
                        System Ready
                    </span>
        
                </div>
        
        
                <!-- =========================
                     CONTROL BUTTONS
                     ========================= -->
        
                <section class="controls">
        
        
                    <!-- FORWARD -->
        
                    <div class="control-row">
        
                        <div>
        
                            <button
                                class="control-button"
                                aria-label="Move Forward"
        
                                onmousedown="
                                    startMovement('forward')
                                "
        
                                onmouseup="
                                    stopMovement()
                                "
        
                                ontouchstart="
                                    startMovement('forward')
                                "
        
                                ontouchend="
                                    stopMovement()
                                "
        
                                onmouseleave="
                                    stopMovement()
                                "
                            >
                                ▲
                            </button>
        
                            <span class="button-label">
                                Forward
                            </span>
        
                        </div>
        
                    </div>
        
        
                    <!-- LEFT / RIGHT -->
        
                    <div class="control-row">
        
        
                        <div>
        
                            <button
                                class="control-button"
                                aria-label="Turn Left"
        
                                onmousedown="
                                    startMovement('left')
                                "
        
                                onmouseup="
                                    stopMovement()
                                "
        
                                ontouchstart="
                                    startMovement('left')
                                "
        
                                ontouchend="
                                    stopMovement()
                                "
        
                                onmouseleave="
                                    stopMovement()
                                "
                            >
                                ◀
                            </button>
        
                            <span class="button-label">
                                Left
                            </span>
        
                        </div>
        
        
                        <div>
        
                            <button
                                class="control-button"
                                aria-label="Turn Right"
        
                                onmousedown="
                                    startMovement('right')
                                "
        
                                onmouseup="
                                    stopMovement()
                                "
        
                                ontouchstart="
                                    startMovement('right')
                                "
        
                                ontouchend="
                                    stopMovement()
                                "
        
                                onmouseleave="
                                    stopMovement()
                                "
                            >
                                ▶
                            </button>
        
                            <span class="button-label">
                                Right
                            </span>
        
                        </div>
        
        
                    </div>
        
        
                    <!-- BACKWARD -->
        
                    <div class="control-row">
        
                        <div>
        
                            <button
                                class="control-button"
                                aria-label="Move Backward"
        
                                onmousedown="
                                    startMovement('backward')
                                "
        
                                onmouseup="
                                    stopMovement()
                                "
        
                                ontouchstart="
                                    startMovement('backward')
                                "
        
                                ontouchend="
                                    stopMovement()
                                "
        
                                onmouseleave="
                                    stopMovement()
                                "
                            >
                                ▼
                            </button>
        
                            <span class="button-label">
                                Reverse
                            </span>
        
                        </div>
        
                    </div>
        
        
                    <!-- EMERGENCY STOP -->
        
                    <button
                        class="stop-button"
                        onclick="
                            stopMovement()
                        "
                    >
                        ■ &nbsp; STOP
                    </button>
        
        
                </section>
        
        
                <!-- =========================
                     FOOTER
                     ========================= -->
        
                <footer class="footer">
        
                    Robotic Vehicle Navigation System
        
                </footer>
        
        
            </main>
        
        </body>
        
        </html>
        
            """
    return html

so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
so.bind(("", 80))
so.listen(5)

while True:
    try:
        conn, addr = so.accept()
        conn.settimeout(3.0)
        print("Connection made %s" % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print("Content = %s" % request)
        car_lef = request.find("/?action=left")
        car_rig = request.find("/?action=right")
        car_for = request.find("/?action=forward")
        car_bac = request.find("/?action=backward")
        car_sto = request.find("/?action=stop")

        print("\n car =", car_bac)
        print("\n car =", car_for)
        print("\n car =", car_lef)
        print("\n car =", car_rig)
        print("\n car =", car_bac)
        print("\n car_St = ", car_sto)
        # forward
        if car_for == 6:
            print("\n forward \n")
            ma1.on()
            ma2.off()
            mb1.on()
            mb2.off()
            led.on()
        # backward
        if car_bac == 6:
            print("\n backward \n")
            ma1.off()
            ma2.on()
            mb1.off()
            mb2.on()
            led.off()
        # left
        if car_lef == 6:
            print("\n left \n")
            ma1.off()
            ma2.on()
            mb1.off()
            mb2.on()
            led.off()
        # right
        if car_rig == 6:
            print("\n right \n")
            ma1.on()
            ma2.off()
            mb1.on()
            mb2.off()
            led.on()
        # stop
        if car_sto == 6:
            print("\n stop \n")
            ma1.off()
            ma2.off()
            mb1.off()
            mb2.off()
            led.off()
            sleep_ms(100)
            led.on()
            sleep_ms(100)

        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
        print('Connection closed')
