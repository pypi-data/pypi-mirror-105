# bitctrl
## IMPORTANT:
(IF YOUR 'COM' PORT IS DIFFERENT, YOU WILL HAVE TO CHANGE THAT MANUALLY IN THE MODULE SCRIPT)
YOUR MICROBIT WILL HAVE TO HAVE THIS SCRIPT. PASTE IT INTO MAKECODE (OR SOMETHING SIMILAR), TURN IT INTO A .hex FILE - 
AND TRANSFER IT TO YOUR MICROBIT (THIS IS A PYTHON SCRIPT):
``` 
serial.redirect_to_usb()
def on_forever():
    if input.button_is_pressed(Button.AB):
        while input.button_is_pressed(Button.AB):
            serial.write_line("AB")
            pause(500)
    if input.button_is_pressed(Button.A):
        while input.button_is_pressed(Button.A):
            if input.button_is_pressed(Button.B):
                serial.write_line('AB')
                pause(500)
            else:
                serial.write_line("A")
                pause(500)
    if input.button_is_pressed(Button.B):
        while input.button_is_pressed(Button.B):
            if input.button_is_pressed(Button.A):
                serial.write_line('AB')
                pause(500)
            else:
                serial.write_line("B")
                pause(500)
    if input.rotation(Rotation.PITCH):
        serial.write_line(str(input.rotation(Rotation.PITCH))+' PITCH')
        pause(15)
    if input.rotation(Rotation.ROLL):
        serial.write_line(str(input.rotation(Rotation.ROLL))+' ROLL')
        pause(15)
forever(on_forever)

 ```
## EXAMPLE CODE/HOW TO USE IT:
If you plan on using this in pygame, your milliseconds in "pause" should be half of that number,
and then half of that number again; let's say you have 60 fps in pygame, then you will have to divide that by two (which is 30), and then divide
30 by two, which is 15 - hence why I have it pausing for 15 milliseconds


When bitctrl returns something, like 'B', it sends back the string 'B' which you can use for other stuff in your main script(s). Example:

```
from bitctrl import Bitctrl
while True:
    bitctrl = Bitctrl.bitctrl('a','b','c', False)
    if bitctrl == 'B':
        print("epic") 
    if bitctrl == 'A':
        print("epic1")
    if bitctrl == 'AB':
        print("epic2")
```

## Another example using Bitctrl.bitctrl('a','b','c',False)
``` 
from bitctrl import Bitctrl
while True:
    bitctrl = Bitctrl.bitctrl('a','s','d',False)
    if str(bitctrl) != 'None':
        print(bitctrl)
```
## Explanation
When you pass "False" through ``` Bitctrl.bitctrl('a','s','d', False) ```
You tell the module that you do not want to press any keys on your keyboard.
So that means that the module only returns the string of the button you pressed on your microbit.

If you were to write ``` Bitctrl.bitctrl('a','s','d') ```, the module will press the keys you passed through the parameters.
So that means it will return the button you pressed on your microbit, but also press the key resembling the button on your microbit.

## Hotkeys with your keyboard
Since my module is using another module called "keyboard", you can pass through hotkeys like 'ctrl+shift+tab' which will press ctrl+shift+tab - you can use that to shift through tabs on your browser.
To make hotkeys efficient, you will have to change the paused milliseconds on your microbit .hex file - maybe something like ``` pause(100) ```, this will make it so it doesn't shift tabs like crazy.

## HOW TO USE _bit_tilt()
``` _bit_tilt() ``` checks and returns a value depending on how you tilt your microbit. If you tilt your microbit to the left, the module will detect that, and return a value, which you can use later!
## EXAMPLE CODE:
``` 
from bitctrl import Bitctrl
import keyboard
while True:
    bit_tilt = Bitctrl._bit_tilt('UP','DOWN','RIGHT','LEFT')
    if bit_tilt == 'UP':
        keyboard.press('up')
    if bit_tilt == 'DOWN':
        keyboard.press('down')      
    if bit_tilt == 'RIGHT':
        keyboard.press('d')
    if bit_tilt == 'LEFT':
        keyboard.press('a') 
```