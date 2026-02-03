from PIL import Image

def main():
    img = Image.open("test.png")
    pixels = array_2d(img,img.size)
    brightness = brightness_array(pixels)

def array_2d(image,size):  
    d2 = []
    for lines in range(0,size[1]):
        d1 = list(image.get_flattened_data()[274*lines:size[0]*(lines+1)])
        d2.append(d1)
    return d2

if __name__ == "__main__":
    main()
