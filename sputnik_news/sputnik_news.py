import os
import shutil
from tkinter import *
from tkinter.scrolledtext import ScrolledText

import requests
from PIL import ImageTk, Image
from bs4 import BeautifulSoup

# main page url
url = "https://tr.sputniknews.com/archive/"
# get page html code
page = requests.get(url)
# create soup object for main page
soup = BeautifulSoup(page.content, "html.parser")
# find all li element
# every element mean one news
news_li = soup.find_all("li", class_="b-plainlist__item")
# news release date
# news_dates = [new.find("span", "b-plainlist__date").text for new in news_list]
# news detail list
news_detail_links = [new.find("div", "b-plainlist__img").a["href"] for new in news_li]
# news title list
news_titles = [new.find("h2", "b-plainlist__title").text for new in news_li]
#
news_infos = [new.find("div", "b-plainlist__announce").text for new in news_li]


def open_detailed_window(link):
    # article page url
    article_url = "https://tr.sputniknews.com" + link
    print(article_url)
    # article page html
    article_page = requests.get(article_url)
    # create soup object for article page
    article_soup = BeautifulSoup(article_page.content, "lxml")
    # body part of article
    article_div = article_soup.find("div", class_="b-article")
    # article title text
    # more detailed then main page title
    article_title = article_div.find("div", "b-article__lead").text.replace('\n','')
    # article detailed text including news details
    article_detail = article_div.find("div", "b-article__text").text

    # create a new window can open over the main window
    new_win = Toplevel(root)
    new_win.geometry("1000x1000")
    new_win.resizable(0, 0)

    # create a canvas for movable text like newscast
    canvas = Canvas(new_win, bg='black')
    canvas.pack()
    canvas.create_text(0, -200, text=article_title,
                       font=('Times New Roman', 30, 'bold'),
                       fill='white',
                       tags=("marquee",), anchor='w')
    # get canvas dimensions for editing for animation
    x1, y1, x2, y2 = canvas.bbox("marquee")
    width = x2 - x1
    height = y2 - y1
    canvas['width'] = width
    canvas['height'] = height
    # moving speed of title text right to left
    anim_speed = 100

    # article image url
    # image size = 1000x541
    article_img_url = article_soup.find("div", "b-article__header").img["src"]
    print(article_img_url)

    # get image saved name with saved folder and image name stored at server
    saved_img_name = os.path.join("articles_img", article_img_url.split("/")[-1].replace(":", "_"))

    # download article image if not stored
    if not os.path.exists(saved_img_name):
        # get image stream
        r = requests.get(article_img_url, stream=True)
        # check image available
        if r.status_code == 200:
            # when we not set true image file will be 0 byte
            r.raw.decode_content = True
            with open(saved_img_name, "wb") as f:
                # save getting img to device
                shutil.copyfileobj(r.raw, f)

    # load image available for tkinter
    photo = ImageTk.PhotoImage(Image.open(saved_img_name))

    # create article image
    Label(new_win, image=photo, width=1000).pack()

    # create scrollable text for article detail using with mouse wheel
    txt = ScrolledText(new_win, font="arial 20")
    txt.pack()
    # add article detail text
    txt.insert(INSERT, article_detail)
    txt.configure(state="disabled")

    def right2left_news_title():
        # get current dimensions
        x1, y1, x2, y2 = canvas.bbox("marquee")
        if (x2 < 0 or y1 < 0):
            x1 = canvas.winfo_width()
            y1 = canvas.winfo_height() // 2
            canvas.coords("marquee", x1, y1)
        else:
            canvas.move("marquee", -2, 0)
        # run method always
        canvas.after(1000 // anim_speed, right2left_news_title)

    # call method one time,after that will be run always when close the window
    right2left_news_title()
    new_win.mainloop()


if __name__ == '__main__':
    # main windows
    root = Tk()
    root.title("Sputnik News")
    # disable resizable
    root.resizable(0, 0)
    root.configure(bg="black")
    
    # sputnik news logo.png
    img = ImageTk.PhotoImage(Image.open("img\logo.png"))
    Label(root, image=img, bg="black").pack()
    # breaking news label
    Label(root, text="Breaking News!", font="Arial 50 bold underline", fg="orange", bg="black").pack()
    # store created buttons else not displaying
    news_btn_list = []
    # number of news is 14 on breaking news page
    for index in range(14):
        #create dynamic btn for everynews
        news_btn_list.append(
            Button(root,
                   text=news_titles[index],
                   font="Arial 15 bold",
                   bg="black", fg="white",
                   command=lambda k=index: open_detailed_window(news_detail_links[k]))
        )
        news_btn_list[index].pack()
        
    root.mainloop()
