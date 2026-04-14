import numpy as np
import colorama
import cv2 as cv
from PIL import Image
import sys, os, time, math

colorama.init()

formats = ['jpeg','png','mp4','avi']

#ascii_chars = np.array(list(" .`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"))
#ascii_chars = np.array(list("$@%#*|1+=-:^. "[::-1]))  #numpy array cause its fast
ascii_chars = np.array(list("$@%&#0Ox/\\|1*+~=-!:,\"^. "[::-1]))  #numpy array cause its fast

maps = len(ascii_chars)-1

def main():
    if len(sys.argv) > 5 or len(sys.argv) < 2:
        sys.exit("Incorrect usage.\nuse:- filename.py image.png/video.mp4")
    if os.path.exists(sys.argv[1]):
        #if ".mkv" in sys.argv[1].lower():
        play_video(sys.argv[1])
        if "png" in sys.argv[1].lower():
            convert_frame_to_ascii(sys.argv[1])
    else:
        sys.exit("File does not exists")


def play_video(video):
    cap = cv.VideoCapture(video)
    fps = cap.get(cv.CAP_PROP_FPS)
    if fps < 24:
        fps = 24
    frame_duration = 1/fps
    next_frame_time = time.perf_counter()
    while True:
        ret,frame = cap.read()
        if not ret:
            sys.stdout.write("END")
            break
        #cv.imshow("current frame",frame)
        sys.stdout.write(f"\033[H\r{(convert_frame_to_ascii(frame))}")
        sys.stdout.flush()
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
    img, width = set_terminal_size(frame)
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    indices = (gray_img.astype(float) / 255 * maps).astype(int)
    ascii_array = ascii_chars[indices]
    lines = ["|" + "".join(row) + "|" for row in ascii_array]
    border = " " + "=" * width
    return f"{border}\n" + "\n".join(lines) + f"\n{border}"


def set_terminal_size(frame):
    frame_aspect_ratio = frame.shape[1]/frame.shape[0]  #frame.shape = (height,width)
    terminal_size = os.get_terminal_size()  #os.get_terminal_size() = (width,height)
    if 0.75 <= frame_aspect_ratio <= 1.35:
        height = terminal_size[1] - 4
        width = height * 2.5 
    elif 1.35 < frame_aspect_ratio:
        width = terminal_size[0] - 4
        height = terminal_size[1] - 4
    elif 0.5 <= frame_aspect_ratio < 0.75:
        width = terminal_size[0] - 20
        height = width * 0.75
    elif frame_aspect_ratio < 0.5:
        width = terminal_size[0] - 50
        height = width * 1
    return cv.resize(frame,(round(width),round(height))),round(width)


if __name__ == "__main__":
    main()
