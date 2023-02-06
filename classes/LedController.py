from ast import Import
import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 20)




class ledController:
    def __init__(self, pixels,id , red, green, blue, pixel_count, isOn, rainbow):
        self.pixels = pixels
        self.id = id
        self.red = self.checkValues(red)
        self.green = self.checkValues(green)
        self.blue = self.checkValues(blue)
        if isOn is not None:
            self.isOn = isOn
        else:
            self.isOn = False
        if rainbow is not None:
            self.rainbow = False
        else:
            self.rainbow = False
        self.pixel_count = pixel_count
        
        
    def __del__(self):
        print('Destructor called, ledController deleted.')
    def led_on(self):
        if self.isOn == True:
            self.isOn = False
            self.toggle()
        else:
            print("The led is already on")  
    
    def led_off(self):
        if self.isOn == False:
            self.isOn = True
            self.toggle()
        else:
            print("The led is already off")
    def toggle( self):
        if(self.isOn == True):
            self.isOn = False
            for i in range (self.pixel_count):
                self.pixels[i] = (0, 0, 0)
                pixels.show()
        elif (self.isOn == False):
            self.isOn = True
            for i in range (self.pixel_count):
                self.pixels[i] = (self.red, self.green, self.blue)
                pixels.show()

    @staticmethod
    def checkValues(value):
        if(value >= 0 and value <= 255):
            return value
        else:
            return 0
    def change_color_value(self):
    #ask for a color for red, green, and blue 
    #return the color
        self.red = int(input("Enter a value for red: "))
        self.green = int(input("Enter a value for green: "))
        self.blue = int(input("Enter a value for blue: "))
        if self.red > 255 or self.green > 255 or self.blue > 255:
            print("Invalid color value")
            self.change_color_value()
        else:
            print("Color value changed")
            ledController.led_on(self)
            return self.red, self.green, self.blue
    def change_color(self, red, green, blue):
        self.led_off()
        self.red = self.checkValues(red)
        self.green = self.checkValues(green)
        self.blue = self.checkValues(blue)
        for i in range (self.pixel_count):
                self.pixels[i] = (self.red, self.green, self.blue)
                pixels.show()
        self.led_on()
    def change_pixel_count(self, pixel_count):
        self.pixel_count = pixel_count
        self.led_on()

    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return (r, g, b) 


    def rainbow_cycle(self):
       #create a thread to run this function
        while self.rainbow:
         for j in range(255):
            for i in range(self.pixel_count):
                pixel_index = (i * 256 // self.pixel_count) + j
                pos = pixel_index & 255
                pixels[i] = self.wheel(pos)
            pixels.show()
            
    def saveLedDetails(self):
        data = {
            "red": self.red,
            "green": self.green,
            "blue": self.blue,
            "isOn": self.isOn,
            "pixel_count": self.pixel_count

        }
        return data

    
    