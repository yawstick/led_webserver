import machine
from machine import Pin
import neopixel
import network
import uasyncio as asyncio
import usocket as socket
import ujson

n = 90
p = 16

np = neopixel.NeoPixel(machine.Pin(p), n)

def set_color(r, g, b):
    for i in range(n):
        np[i] = (r, g, b)
    np.write()

# Your LED control functions go here
def turn_on_red_led():
    set_color(100, 0, 0)
    print("Red LED turned on")

def turn_on_blue_led():
    set_color(0, 0, 100)
    print("Blue LED turned on")

def turn_on_green_led():
    set_color(0, 100, 0)
    print("Green LED turned on")
    
def turn_on_sky_led():
    set_color(0, 100, 100)
    print("sky LED turned on")
    
def turn_on_clear_led():
  for i in range(n):
    np[i] = (0, 0, 0)
    np.write()
    

# Request handler for handling incoming HTTP requests
# Request handler for handling incoming HTTP requests
async def handle_request(reader, writer):
    try:
        request = await reader.read(4096)
        request_str = request.decode("utf-8")
        print("Received request:", request_str)

        # Extract the color from the request data
        color = request_str.split('_button=on')[0]

        if request_str.startswith('GET'):
            # Serve the HTML file
            with open('www/led.html', 'r') as f:
                html_content = f.read()
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{html_content}"
        else:
            if "red" in color:
                turn_on_red_led()
            elif "blue" in color:
                turn_on_blue_led()
            elif "green" in color:
                turn_on_green_led()
            elif "sky" in color:
                turn_on_sky_led()
            elif "clear" in color:
                turn_on_clear_led()    

            # Send a simple response back to the client
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nLED control successful for {color}!"
        
        await writer.awrite(response)
    except Exception as e:
        print("Error handling request:", e)
    finally:
        await writer.aclose()

# Create an asyncio event loop
loop = asyncio.get_event_loop()

# Start the HTTP server
loop.create_task(asyncio.start_server(handle_request, "0.0.0.0", 80))

# Run the event loop
loop.run_forever()

