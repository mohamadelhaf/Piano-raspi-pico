try:
 import usocket as socket        #importing socket
except:
 import socket
import network            #importing network
import gc
import time
from machine import PWM, Pin

gc.collect()
ssid = 'RPI_PICO_AP'                  #Set access point name 
password = '12345678'      #Set your access point password


ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)            #activating

while ap.active() == False:
  pass
print('Connection is successful')
print(ap.ifconfig())
BUZZER_PIN = 0

# Define the piano note frequencies
NOTES = {
    'C': 261,
    'D': 294,
    'E': 329,
    'F': 349,
    'G': 391,
    'A': 440,
    'B': 493,
}

# Define the duration of each note
DURATION = 0.5

# Initialize the PWM object
pwm = PWM(Pin(BUZZER_PIN, mode=Pin.OUT))

# Define a function to play a single note
def play_note(note):
    # Get the frequency of the note
    frequency = NOTES[note]
    
    # Set the duty cycle of the PWM to 50%
    pwm.duty_u16(32768)
    
    # Set the frequency of the PWM to the note's frequency
    pwm.freq(frequency)
    
    # Wait for the duration of the note
    time.sleep(DURATION)
    
    # Stop the PWM
    pwm.deinit()



def web_page():
  html = """<!DOCTYPE html>
<html>
<head>
    <title>Piano</title>
</head>
<body>
    <h1>Piano</h1>
    <button onclick="play('C')">C</button>
    <button onclick="play('D')">D</button>
    <button onclick="play('E')">E</button>
    <button onclick="play('F')">F</button>
    <button onclick="play('G')">G</button>
    <button onclick="play('A')">A</button>
    <button onclick="play('B')">B</button>
    <script>
        function play(note) {
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      play_note(note);
    }
  };
  xhttp.open("GET", "/?note=" + note, true);
  xhttp.send();
}

    </script>
</body>
</html>"""
  return html

def handle_Request(request):
    print('Request:', request)  # print the contents of the request to the console
    if "/?note=" in request:
        note = request.split("/?note=")[1].split(" ")[0]
        play_note(note)
    return web_page()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
s.bind(('', 80))
s.listen(5)

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  print('Content = %s' % str(request))
  # Handle /play_buzzer endpoint
  if '/play_note' in str(request):
        play_note()
        response = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'
  else:
        response = web_page()
        
  conn.send(response)
  conn.close()