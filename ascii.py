import os
import sys
import math
from PIL import Image
from statistics import mean

def main():
    if len(sys.argv) > 2 or len(sys.argv) < 2:
        sys.exit("Incorrect usage.\nuse:- filename.py image.png")
    try:
        img = Image.open(sys.argv[1])
    except FileNotFoundError:
        sys.exit("File does not exists")
    else:
        size = ratio(img.size) 
        img = img.resize(size)
        os.system(f"mode con:cols={size[0]+5} lines={size[1]+5}")
        pixels = array_2d(img,img.size)
        brightness = brightness_array(pixels)
        mapped = mapping(brightness)
        display(mapped,img.size)

def ratio(size):
    width = 165
    height = (size[1]/size[0]) * 100
    return (width,int(height))

def array_2d(image,size):  
    d2 = []
    for lines in range(0,size[1]):
        d1 = list(image.get_flattened_data()[size[0]*lines:size[0]*(lines+1)])
        d2.append(d1)
    return d2

def brightness_array(pixel_array):
    d2 = []
    for row in pixel_array:
        d1 = []
        for column in row:
            d1.append(int(percieved_brightness(column)))
        d2.append(d1)
    return d2

def percieved_brightness(values):
    r = values[0]
    g = values[1]
    b = values[2]
    return math.sqrt((0.241*r*r)+(0.691*g*g)+(0.068*b*b))

def mapping(brightness):
    #string = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    string = "$@%#*|1+=-:^."[::-1]
    d2 = []
    for row in brightness:
        d1 = []
        for column in row:
            d1.append(string[mapped_value(column,len(string))])
        d2.append(d1)
    return d2

def mapped_value(value,length):
    a = round((value*length)/ 255)
    if a >= length:
        a = length - 1
    return a

def display(mapped_array,size):
    for line in mapped_array:
        for c in line:
            print(c*1,end="")
        print("")
    print(size)

if __name__ == "__main__":
    main()



