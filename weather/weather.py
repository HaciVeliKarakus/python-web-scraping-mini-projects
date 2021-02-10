import os
import shutil
from tkinter import *

import requests
from PIL import ImageTk, Image


class Expandable_Map(Frame):
    """this is a frame with a label, can resizable with map image"""
    def __init__(self, master, map_save_name, *pargs):
        Frame.__init__(self, master, *pargs)
        # load map image
        self._img_load(map_save_name)

        # create photo with giving map image
        self.photo = ImageTk.PhotoImage(self.image)
        # create a label for showing map image
        self.map = Label(self, image=self.photo)
        self.map.pack(fill=BOTH, expand=YES)
        # binding to resize method,call when resize window
        self.map.bind('<Configure>', self._resize_image)

    def _img_load(self, img):
        """load and store image"""
        self.image = Image.open(img)
        self.img_copy = self.image.copy()

    def _resize_image(self, event):
        """get new dimension and reload showing map image"""
        self.new_width = event.width
        self.new_height = event.height

        self._reload_map()

    def _reload_map(self):
        """resize map image with new size"""
        self.image = self.img_copy.resize((self.new_width, self.new_height))
        self.photo = ImageTk.PhotoImage(self.image)
        self.map.configure(image=self.photo)

    def map_change(self, img):
        """to change map image outside"""
        self._img_load(img)
        self._reload_map()


def prepare_save_folder(num):
    # create maps folder for store downloaded map image
    if not os.path.exists('maps'):
        os.makedirs('maps')
    # create map url with number
    map_url = "https://www.mgm.gov.tr/FTPDATA/analiz/harita/png/haritatahmingun" + str(num) + ".png"
    # get image name original name
    map_name = map_url.split('/')[-1]
    map_save_name = "maps/" + map_name
    if not os.path.exists(map_save_name):
        # get image stream
        r = requests.get(map_url, stream=True)
        # check image available
        if r.status_code == 200:
            # when we not set true image file will be 0 byte
            r.raw.decode_content = True
            with open(map_save_name, "wb") as f:
                # save getting img to device
                shutil.copyfileobj(r.raw, f)

    return map_save_name


def change_map(day):
    e.map_change(prepare_save_folder(day))


if __name__ == '__main__':
    root = Tk()
    root.geometry("790x381")
    root.title("WEATHER")

    map_save_name = prepare_save_folder(1)

    e = Expandable_Map(root, map_save_name)
    e.pack(fill=BOTH, expand=YES)

    days = []

    menubar = Menu(root)

    menubar.add_command(label="BUGÜN", command=lambda: change_map(1))
    menubar.add_command(label="YARIN", command=lambda: change_map(2))
    menubar.add_command(label="2 GÜN SONRA", command=lambda: change_map(3))
    menubar.add_command(label="3 GÜN SONRA", command=lambda: change_map(4))
    menubar.add_command(label="4 GÜN SONRA", command=lambda: change_map(5))
    root.config(menu=menubar)

    root.mainloop()
