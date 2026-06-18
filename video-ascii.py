import colorama
import numpy as np
import cv2
from tkinter.filedialog import askopenfilename
import sys, os, time

colorama.init()


class ASCII:
    def __init__(self, video,webcam = 0):
        self.ascii_chars = np.array(list('$@%&#0Ox/\\|1*+~=-!:,"^. '[::-1]))
        self.maps = len(self.ascii_chars) - 1
        self.char_indices = None
        self.video = video
        self.fps = 0
        self.frame_duration = 0
        self.cap = None
        self.ascii_str = []
        self.webcam = webcam

    def getfps(self):
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        return fps if fps > 24 else 24

    def play_video(self):
        next_frame_time = time.perf_counter()
        while True:
            ret, frame = self.cap.read()
            if not ret:
                sys.stdout.write("END")
                sys.stdout.flush()
                break
            # cv.imshow("current frame",frame)
            sys.stdout.write(f"\033[H\r{self.convert_frame_to_ascii(frame)}")
            sys.stdout.flush()
            next_frame_time += self.frame_duration
            sleep_time = next_frame_time - time.perf_counter()
            if sleep_time > 0:
                time.sleep(sleep_time)
            if cv2.waitKey(1) == ord("q"):
                break

    def convert_frame_to_ascii(self, frame):
        self.img, width = self.set_terminal_size(frame)
        self.set_ascii_setup()
        lines = ["|" + "".join(row) + "|" for row in self.ascii_str]
        border = " " + "=" * width
        return f"{border}\n" + "\n".join(lines) + f"\n{border}"

    def set_terminal_size(self, frame):
        frame_aspect_ratio = (
            frame.shape[1] / frame.shape[0]
        )  # frame.shape = (height,width)
        terminal_size = (
            os.get_terminal_size()
        )  # os.get_terminal_size() = (width,height)
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
        else:
            width = frame.shape[0]
            height = frame.shape[1]
        img = cv2.resize(frame, (round(width), round(height)))
        return img, round(width)

    def set_ascii_setup(self):
        gray_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.char_indices = (gray_img.astype(float) / 255 * self.maps).astype(int)
        self.ascii_str = self.ascii_chars[self.char_indices]

    def setup(self):
        video = self.video
        self.cap = cv2.VideoCapture(video)
        self.fps = self.getfps()
        self.frame_duration = 1 / self.fps

    def end(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def start(self):
        self.setup()
        self.play_video()
        self.end()


def main():
    try:
        mode = int(input("Enter Mode:\n1. Video\n2. Webcam\n: "))
    except TypeError:
        sys.exit("Enter Proper Mode")
    else:
        if mode == 1:
            video = ASCII(askopenfilename())
        else:
            video = ASCII(0,1)
    video.start()


if __name__ == "__main__":
    main()
