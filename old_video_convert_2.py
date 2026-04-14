import colorama
from rich.console import Console
from rich.text import Text
import numpy as np
import cv2 as cv
from PIL import Image
import sys, os, time, math

colorama.init()

formats = ['jpeg','png','mp4','avi']

#ascii_chars = " .`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
#ascii_chars = np.array(list("$@%#*|1+=-:^. "[::-1]))
ascii_chars = np.array(list("$@%&#0Ox/\\|1*+~=-!:,\"^. "[::-1]))  #numpy array cause its fast

maps = len(ascii_chars)-1

def main():
    if len(sys.argv) > 5 or len(sys.argv) < 2:
        sys.exit("Incorrect usage.\nuse:- filename.py image.png/video.mp4")
    if os.path.exists(sys.argv[1]):
        if ".mp4" in sys.argv[1].lower():
            play_video(sys.argv[1])
        elif "png" in sys.argv[1].lower():
            convert_frame_to_ascii(sys.argv[1])
    else:
        sys.exit("File does not exists")


def play_video(video):
    console = Console()
    cap = cv.VideoCapture(video)
    fps = cap.get(cv.CAP_PROP_FPS)
    if fps <= 0:
        fps = 24
    frame_duration = 1/fps
    next_frame_time = time.perf_counter()
    while True:
        ret,frame = cap.read()
        if not ret:
            sys.stdout.write("END")
            break
        cv.imshow("current frame",frame)
        sys.stdout.write(f"\033[H\r{(convert_frame_to_ascii(frame))}")
        sys.stdout.flush()
#        console.clear()
#        console.print(convert_frame_to_ascii(frame))
        convert_frame_to_ascii(frame)
        next_frame_time += frame_duration
        sleep_time = next_frame_time - time.perf_counter()
        if sleep_time > 0 :
            time.sleep(sleep_time)
        if cv.waitKey(1) == ord("q"):
            break
    cap.release()
    cv.destroyAllWindows()


#For bad apple width = 105
#For ellen joe width = 165
def convert_frame_to_ascii(frame):
    img, width, height = set_terminal_size(frame)
    
    # 1. Faster color conversion and index mapping
    # We use gray for char selection and RGB for the actual color
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    rgb_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    
    # Pre-calculate all character indices at once using NumPy
    char_indices = (gray_img.astype(np.float32) / 255 * maps).astype(np.int32)
    
    ascii_str = []
    border = " " + "=" * width + "\n"
    ascii_str.append(border)
    
    # Track current color to minimize ANSI overhead
    curr_r, curr_g, curr_b = -1, -1, -1
    
    for row in range(height):
        ascii_str.append("|")
        for col in range(width):
            r, g, b = rgb_img[row, col]
            char = ascii_chars[char_indices[row, col]]
            
            if char == " ":
                ascii_str.append(char)
                continue
            
            # Only change color if it's different from the last pixel
            if (r, g, b) != (curr_r, curr_g, curr_b):
                ascii_str.append(f"\033[38;2;{r};{g};{b}m{char}")
                curr_r, curr_g, curr_b = r, g, b
            else:
                ascii_str.append(char)
                
        ascii_str.append("\033[0m|\n") # Reset color at end of line
        curr_r, curr_g, curr_b = -1, -1, -1 # Reset for new line tracking
        
    ascii_str.append(border)
    return "".join(ascii_str)


def color_code(r,g,b):
    r_idx = int(r/256*6)
    g_idx = int(g/256*6)
    b_idx = int(b/256*6)
    return 16+(36*r_idx) + (6*g_idx) + b_idx


def set_terminal_size(frame):
    frame_aspect_ratio = frame.shape[1]/frame.shape[0]  #frame.shape = (heigth,width)
    terminal_size = os.get_terminal_size()  #os.get_terminal_size() = (width,heigth)
    if 0.75 <= frame_aspect_ratio <= 1.35:
        heigth = terminal_size[1] - 4
        width = heigth * 2.5 
    elif 1.35 < frame_aspect_ratio:
        width = terminal_size[0] - 4
        heigth = terminal_size[1] - 4
    elif 0.5 <= frame_aspect_ratio < 0.75:
        width = terminal_size[0] - 20
        heigth = width * 0.75
    elif frame_aspect_ratio < 0.5:
        width = terminal_size[0] - 50
        heigth = width * 1
    return cv.resize(frame,(round(width),round(heigth))),round(width),round(heigth)

if __name__ == "__main__":
    main()
