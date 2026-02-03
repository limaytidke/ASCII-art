from PIL import Image
from statistics import mean

def main():
    img = Image.open("test.png")
    img = img.resize((185,50))
    pixels = array_2d(img,img.size)
    brightness = brightness_array(pixels)
    mapped = mapping(brightness)
    display(mapped)

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
            d1.append(int(mean([column[0],column[1],column[2]])))
        d2.append(d1)
    return d2

def mapping(brightness):
    string = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    d2 = []
    for row in brightness:
        d1 = []
        for column in row:
            d1.append(string[mapped_value(column)])
        d2.append(d1)
    return d2

def mapped_value(value):
    return round((value*65)/ 255)

def display(mapped_array):
    for line in mapped_array:
        for c in line:
            print(c*1,end="")
        print("")

if __name__ == "__main__":
    main()



