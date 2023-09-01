import tkinter as tk
from tkinter import *
import pyautogui
import datetime
import dxcam
from PIL import Image
import logging
import threading
import time
from collections import deque
from fuzzychinese import FuzzyChineseMatch
import re

from translate import translate
from ocr import perform_ocr
from variables import OCR_DEBUG

camera = dxcam.create()



def filter_chinese(context, keep_numbers=True):
    if keep_numbers:
        filtrate = re.compile(u'[^\u4E00-\u9FA51234567890]') # non-Chinese unicode range
    else:
        filtrate = re.compile(u'[^\u4E00-\u9FA5]')  # non-Chinese unicode range
    context = filtrate.sub(r'', context) # remove all non-Chinese characters
    return context




#https://stackoverflow.com/questions/49901928/how-to-take-a-screenshot-with-python-using-a-click-and-drag-method-like-snipping
class Application():
    def __init__(self, master):
        self.snip_surface = None
        self.master = master
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None
        self.message_queue = deque()
        self.detected_text_list = []
        self.translated_text_list = []

        #root.geometry('400x50+200+200')  # set new geometry
        #root.title('Bilibili translate project')
        root.update_idletasks()
        root.overrideredirect(True)
        root.attributes('-topmost', True)

        self.menu_frame = Frame(master)
        self.menu_frame.pack(fill=BOTH, expand=YES, padx=0, pady=0)

        self.title_bar = Frame(master, bg='darkgreen', relief=tk.RAISED, bd=0)
        self.title_bar.pack(fill=tk.X, expand=1, side=tk.BOTTOM)
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<ButtonRelease-1>", self.stop_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)

        self.title_label = tk.Label(self.title_bar, text='Bilibili translate project', bg='darkgreen', fg='white')
        self.title_label.pack(fill=tk.X, side=tk.LEFT, pady=2)

        self.close_label = tk.Label(self.title_bar, text='  X  ', bg='darkgreen', fg='white', relief=tk.SUNKEN)
        self.close_label.pack(side=tk.RIGHT, pady=2)
        self.close_label.bind("<Button-1>", quit_app)

        # Create a transparent window
        #root.wm_attributes('-transparentcolor', '#add123')

        self.text = tk.Label(self.menu_frame, text="",
                             wraplength=480, width=30, height=3, pady=1, font=("Arial", 16))
        self.text.pack(expand=True)


        self.buttonBar = Frame(self.menu_frame, bg="")
        self.buttonBar.pack()

        self.snipButton = Button(self.buttonBar, padx=1, width=10, height=1, relief=tk.RAISED,
                                 text="Select region", command=self.create_screen_canvas) #, background="blue"
        self.snipButton.pack(fill=tk.Y, side=tk.LEFT)

        self.translateButton = Button(self.buttonBar, padx=1, width=10, height=1,
                                      text="Begin translate", command=self.start_ocr, background="green")
        self.translateButton.pack(fill=tk.Y, side=tk.LEFT)

        self.stopButton = Button(self.buttonBar, padx=1, width=10, height=1,
                                 text="Stop", command=self.stop_ocr, background="red")
        self.stopButton.pack(fill=tk.Y, side=tk.LEFT)



        self.master_screen = Toplevel(root)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "maroon3")
        self.picture_frame = Frame(self.master_screen, background="maroon3")
        self.picture_frame.pack(fill=BOTH, expand=YES)


    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = root.winfo_x() + deltax #event.x_root
        y = root.winfo_y() + deltay #event.y_root
        root.geometry(f"+{x}+{y}")

    def create_screen_canvas(self):
        self.master_screen.deiconify()
        root.withdraw()

        self.snip_surface = Canvas(self.picture_frame, cursor="cross", bg="grey11")
        self.snip_surface.pack(fill=BOTH, expand=YES)

        self.snip_surface.bind("<ButtonPress-1>", self.on_button_press)
        self.snip_surface.bind("<B1-Motion>", self.on_snip_drag)
        self.snip_surface.bind("<ButtonRelease-1>", self.on_button_release)

        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', .3)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def on_button_release(self, event):
        self.display_rectangle_position()

        self.start_capture(self.start_x, self.start_y, self.current_x, self.current_y)
        #if self.start_x <= self.current_x and self.start_y <= self.current_y:
        #    print("right down")
        #    take_bounded_screenshot(self.start_x, self.start_y, self.current_x - self.start_x, self.current_y - self.start_y)
#
        #elif self.start_x >= self.current_x and self.start_y <= self.current_y:
        #    print("left down")
        #    take_bounded_screenshot(self.current_x, self.start_y, self.start_x - self.current_x, self.current_y - self.start_y)
#
        #elif self.start_x <= self.current_x and self.start_y >= self.current_y:
        #    print("right up")
        #    take_bounded_screenshot(self.start_x, self.current_y, self.current_x - self.start_x, self.start_y - self.current_y)
#
        #elif self.start_x >= self.current_x and self.start_y >= self.current_y:
        #    print("left up")
        #    take_bounded_screenshot(self.current_x, self.current_y, self.start_x - self.current_x, self.start_y - self.current_y)

        self.exit_screenshot_mode()
        return event

    def exit_screenshot_mode(self):
        self.snip_surface.destroy()
        self.master_screen.withdraw()
        root.deiconify()

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.snip_surface.canvasx(event.x)
        self.start_y = self.snip_surface.canvasy(event.y)
        self.snip_surface.create_rectangle(0, 0, 1, 1, outline='red', width=3, fill="maroon3")

    def on_snip_drag(self, event):
        self.current_x, self.current_y = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.snip_surface.coords(1, self.start_x, self.start_y, self.current_x, self.current_y)

    def display_rectangle_position(self):
        pass
        #print(self.start_x)
        #print(self.start_y)
        #print(self.current_x)
        #print(self.current_y)

    def start_capture(self, x1, y1, x2, y2):
        x1 = int(x1)
        y1 = int(y1)
        x1, x2 = (int(min(x1, x2)), int(max(x1, x2)))
        y1, y2 = (int(min(y1, y2)), int(max(y1, y2)))

        # image = pyautogui.screenshot(region=(x1, y1, x2, y2))
        camera.stop()
        camera.start(region=(x1, y1, x2, y2), target_fps=10, video_mode=True)
        #

    def handle_capture(self):
        x = 0
        while camera.is_capturing and x<100000:
            x += 1
            try:
                image = camera.get_latest_frame()  # Will block until new frame available
            except TypeError:
                continue

            detected_text = perform_ocr(image, debug=OCR_DEBUG)
            detected_text = filter_chinese(detected_text)
            if len(filter_chinese(detected_text, keep_numbers=False)) == 0:
                continue

            sim = 0
            if len(self.detected_text_list) >= 1:
                if len(self.detected_text_list) >= 2:
                    recent = self.detected_text_list[-2:]
                else:
                    recent = [self.detected_text_list[-1]]

                recent = [filter_chinese(x, keep_numbers=False) for x in recent]
                fcm = FuzzyChineseMatch(ngram_range=(3, 3), analyzer='stroke')
                fcm.fit(recent)
                fcm.transform([filter_chinese(detected_text, keep_numbers=False)], n=2)
                sim = max(fcm.get_similarity_score()[0])

            if len(self.detected_text_list) <= 0 or sim < 0.93:
                self.detected_text_list.append(detected_text)
                translated_text = translate(detected_text)
                self.translated_text_list.append(translated_text)
                self.message_queue.append(translated_text)

    def start_ocr(self):
        if camera.is_capturing:
            x = threading.Thread(target=self.handle_capture, args=())
            x.setDaemon(True)
            x.start()
        else:
            print("Camera is not capturing!")
        # x.join()

    def stop_ocr(self):
        camera.stop()
    def consume_text(self):
        try:
            self.text["text"] = self.message_queue.popleft()
        except (IndexError, tk.TclError):
            pass  # Ignore, if no text available.
        # Reschedule call to consumeText.
        root.after(ms=100, func=self.consume_text)

def move_app(e):
    root.geometry(f'+{e.x_root}+{e.y_root}')
def quit_app(e):
    root.quit()

if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    app.consume_text()
    root.mainloop()
    camera.stop()

    file_name = "translations/"+datetime.datetime.now().strftime("%Y_%m_%d-%H_%M") + "-translog.txt"
    with open(file_name, 'w', encoding="utf-8") as fp:
        text = [app.detected_text_list[i] + " : " + app.translated_text_list[i] for i in range(len(app.detected_text_list))]
        fp.write('\n'.join(text))