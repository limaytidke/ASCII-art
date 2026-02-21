import cv2 as cv
from PIL import Image
import sys, os, time, math

formats = ['jpeg','png','mp4','avi']

#ascii_chars = " .`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
ascii_chars = "$@%#*|1+=-:^. "[::-1]

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
        sys.stdout.write(f"\r{(convert_frame_to_ascii(frame))}")
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
    width = 105
    height = int(frame.shape[1]/frame.shape[0]) * 45
    img = cv.resize(frame,(width,height))
    gray_img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    ascii_str = " " + "="*width + "\n"
    for row in gray_img:
        ascii_str += "|"
        for col in row:
            mapped_value = (col/255) * maps
            ascii_str += ascii_chars[int(mapped_value)]
        ascii_str += "|\n"
    ascii_str += " " + "="*width + "\n"
    return ascii_str


if __name__ == "__main__":
    main()
