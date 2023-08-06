IMPORTANT:
TO USE THIS WITH MICROBIT, YOUR MICROBIT WILL HAVE TO TURN THIS PYTHON SCRIPT INTO A .hex FILE AND INSTALL IT ON TO YOUR MICROBIT:

 serial.redirect_to_usb()
 def on_forever():
     if input.button_is_pressed(Button.AB):
         while input.button_is_pressed(Button.AB):
             serial.write_line("A")
             pause(15)
     if input.button_is_pressed(Button.A):
         while input.button_is_pressed(Button.A):
             serial.write_line("A")
             pause(15)
     if input.button_is_pressed(Button.B):
         while input.button_is_pressed(Button.B):
             serial.write_line("B")
             pause(15)
 forever(on_forever)
If you plan on using this in pygame, your milliseconds in "pause" should be half of that number,
and then half of that number; so if you have 60 fps in pygame, you divide that by two, so 30, then divide
30 by two, which is 15 - hence why I have it pausing for 15 milliseconds

EXAMPLE CODE/HOW TO USE IT:

When bitctrl returns something, like 'B', it sends back the string 'B' which you can use for other stuff in your main script(s). Example:
 from bitctrl import Bitctrl
 while True:
     bitctrl = Bitctrl.bitctrl('a','b','c')
     if bitctrl == 'B':
         print("epic")